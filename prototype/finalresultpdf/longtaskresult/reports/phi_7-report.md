# Closed-loop v2 单模型报告：phi_7 / CC/claude-sonnet-5 (max)

## 身份

| 字段 | 值 |
|---|---|
| protocol | closed-loop-v2-single-model-v1 |
| benchmark copy | closed_loop_v2_single_phi_7_20260726T091835Z |
| slot (manifest) | subtest_14 |
| binding_slot | phi_7 |
| expected_model | CC/claude-sonnet-5 |
| thinking_effort | max（显式配置） |
| agent_id | agent-7（provider 503 后 resume 一次，同一 agent 上下文） |
| pass | Pass@1（无 repair 轮） |

## 主轴结果

| 轴 | 值 |
|---|---|
| InstructionGate | False |
| ClosedLoopProjectCount | 0/2 |
| MilestoneStrictCount | 0/10 |
| AcceptanceCoverage | 0.75 (15/20) |
| decision_infrastructure_indeterminate | False |

## Instruction Gate 细节

- `workspace_non_source`: failed; diagnostics: ['source outside allowed package boundaries: src/__init__.py']
- `process_no_delegation_attempt`: unobservable; diagnostics: Not observable from final workspace files.
- `process_no_hidden_evaluator_read_attempt`: unobservable; diagnostics: Not observable from final workspace files.
- `process_no_network_attempt`: unobservable; diagnostics: AST-visible behavior is audited, but execution history is not observable from final files.
- `writes_only_declared_storage`: unobservable; diagnostics: Final workspace files cannot prove that runtime writes stayed within declared storage.

注：`workspace_non_source` 对 `src/__init__.py` 的失败与 phi_5 / phi_6 / 原十模型轮完全相同，是 audit 规则对 template 自带文件的系统性判定。

## Milestone / criterion

### order_fulfillment (closed_loop_success=False)

- OF1: strict=False (0/2)
  - FAIL OF1-C1 -> closed_loop_v2.evaluator.test_order_fulfillment.OrderPersistenceTests.test_schema_initialize_and_reopen
  - FAIL OF1-C2 -> closed_loop_v2.evaluator.test_order_fulfillment.OrderPersistenceTests.test_input_and_dependency_validation
- OF2: strict=False (2/2)
- OF3: strict=False (2/2)
- OF4: strict=False (2/2)
- OF5: strict=False (2/2)

### delivery_spool (closed_loop_success=False)

- DS1: strict=False (0/2)
  - FAIL DS1-C1 -> closed_loop_v2.evaluator.test_delivery_spool.SpoolPersistenceTests.test_initialize_reopen_and_fail_closed
  - FAIL DS1-C2 -> closed_loop_v2.evaluator.test_delivery_spool.SpoolPersistenceTests.test_canonical_payload_idempotency_and_limits
- DS2: strict=False (2/2)
- DS3: strict=False (1/2)
  - FAIL DS3-C1 -> closed_loop_v2.evaluator.test_delivery_spool.SpoolOutcomeTests.test_ack_and_fail_require_exact_token
- DS4: strict=False (2/2)
- DS5: strict=False (2/2)

## Token usage（仅 agent-7 wire）

| 分量 | 值 |
|---|---|
| input_other | 96 |
| input_cache_read | 11,002,605 |
| input_cache_creation | 416,417 |
| input_context_tokens | 11,419,118 |
| output_tokens | 225,277 |
| fresh_tokens | 641,790 |
| inference_tokens | 11,644,395 |
| usage_record_count | 48 |
| token_measurement_status | valid |
| model_match | True |
| 超过 10M soft SLA | yes |

## 结论

- 候选自报 completed 且全部自validation pass，机械评测 15/20。
- 失败集中在 OF1（2）、DS1（2）、DS3-C1（ack/fail token 授权）；OF2-OF5、DS2 其余、DS4、DS5 通过。
- InstructionGate=false 为 src/__init__.py 系统性判定；严格 milestone 计 0，criterion 原始结果保留。
- token 计量有效，约 11.64M inference tokens，超过 10M 软上限（ResourceSLA=FAIL，事实保留不删除）。
- 执行链有一次 provider 503 后 resume（同一 agent 上下文），如实记录。
- 本报告不构成跨模型排名。
