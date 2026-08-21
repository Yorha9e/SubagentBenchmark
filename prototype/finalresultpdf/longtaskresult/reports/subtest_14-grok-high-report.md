# Closed-loop v2 单模型报告：subtest_14 / grok/grok-4.5 (high)

## 身份

| 字段 | 值 |
|---|---|
| protocol | closed-loop-v2-single-model-v1 |
| benchmark copy | closed_loop_v2_single_subtest_14_grok_high_20260726T140000Z |
| slot (manifest) | subtest_14 |
| binding_slot | subtest_14 |
| expected_model | grok/grok-4.5 |
| thinking_effort | high（显式配置） |
| agent_id | agent-16（首次 provider capacity failure 后重试） |
| pass | Pass@1（本 workspace 无 repair 轮） |

## 主轴结果

| 轴 | 值 |
|---|---|
| InstructionGate | False |
| ClosedLoopProjectCount | 0/2 |
| MilestoneStrictCount | 0/10 |
| AcceptanceCoverage | 0.75 (15/20) |
| decision_infrastructure_indeterminate | False |

## Instruction Gate 细节

- `workspace_non_source`: failed; diagnostics: `source outside allowed package boundaries: src/__init__.py`
- 其余可观察结构检查通过或不可观察。
- `src/__init__.py` 为 template 自带文件；该 Gate 失败与此前 closed-loop-v2 单模型运行中的系统性 audit 判定一致，不代表候选修改了该文件。

## Milestone / criterion

### order_fulfillment (closed_loop_success=False)

- OF1: strict=False (1/2)
  - FAIL OF1-C1 -> `closed_loop_v2.evaluator.test_order_fulfillment.OrderPersistenceTests.test_schema_initialize_and_reopen`
- OF2: strict=False (2/2)
- OF3: strict=False (2/2)
- OF4: strict=False (2/2)
- OF5: strict=False (1/2)
  - FAIL OF5-C2 -> `closed_loop_v2.evaluator.test_order_cli.OrderCliTests.test_error_codes_exit_codes_and_persistence`

### delivery_spool (closed_loop_success=False)

- DS1: strict=False (1/2)
  - FAIL DS1-C2 -> `closed_loop_v2.evaluator.test_delivery_spool.SpoolPersistenceTests.test_canonical_payload_idempotency_and_limits`
- DS2: strict=False (2/2)
- DS3: strict=False (1/2)
  - FAIL DS3-C1 -> `closed_loop_v2.evaluator.test_delivery_spool.SpoolOutcomeTests.test_ack_and_fail_require_exact_token`
- DS4: strict=False (2/2)
- DS5: strict=False (1/2)
  - FAIL DS5-C2 -> `closed_loop_v2.evaluator.test_spool_cli.SpoolCliTests.test_cli_protocol_and_root_boundary`

## Token usage（仅 agent-16 wire）

| 分量 | 值 |
|---|---:|
| input_other | 127,678 |
| input_cache_read | 1,473,802 |
| input_cache_creation | 0 |
| input_context_tokens | 1,473,802 |
| output_tokens | 50,461 |
| fresh_tokens | 178,139 |
| inference_tokens | 1,651,941 |
| usage_record_count | 24 |
| token_measurement_status | valid |
| model_match | True |
| 超过 10M soft SLA | no |

## 结论

- 候选自报 completed；机械评测 15/20。
- 未闭环项目：OF1、OF5、DS1、DS3、DS5 各有 criterion 失败。
- InstructionGate=false 主要来自 template 自带 `src/__init__.py` 的系统性 audit 判定；严格 milestone 因此计 0，criterion 原始结果保留。
- token 计量有效，约 1.65M inference tokens，未超 10M 软上限。
- 首次派发遇到 provider capacity failure，随后使用同一 agent 重试完成；该 transient failure 不计入候选结果。
- 本报告不构成跨模型正式排名；合榜位置见 `closed_loop_v2/results/phi5-phi7-scorecard-for-leaderboard.md`。
