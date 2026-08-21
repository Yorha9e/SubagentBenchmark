# Closed-loop v2 单模型报告：phi_6 / CC/claude-fable-5 (max)

## 身份

| 字段 | 值 |
|---|---|
| protocol | closed-loop-v2-single-model-v1 |
| benchmark copy | closed_loop_v2_single_phi_6_max_20260726T084147Z |
| slot (manifest) | subtest_14 |
| binding_slot | phi_6 |
| expected_model | CC/claude-fable-5 |
| configured_alias | CC/claude-opus-4-8 |
| resolved_model | CC/claude-fable-5（用户确认的实际路由模型） |
| raw_wire_model | CC/claude-opus-4-8（原始 wire 保留） |
| thinking_effort | max（显式配置） |
| agent_id | agent-6（task.lost 后 resume 一次，同一 agent 上下文） |
| 前置中止记录 | agent-2（high effort，用户要求停止，旧目录 closed_loop_v2_single_phi_6_20260726T080741Z 未评测）；agent-3（prompt 路径笔误，启动即停止）；agent-5（502 未开始） |
| pass | Pass@1（本 workspace 无 repair 轮） |

## 主轴结果

| 轴 | 值 |
|---|---|
| InstructionGate | False |
| ClosedLoopProjectCount | 0/2 |
| MilestoneStrictCount | 0/10 |
| AcceptanceCoverage | 0.85 (17/20) |
| decision_infrastructure_indeterminate | False |

## Instruction Gate 细节

- `workspace_non_source`: failed; diagnostics: ['source outside allowed package boundaries: src/__init__.py']
- `process_no_delegation_attempt`: unobservable; diagnostics: Not observable from final workspace files.
- `process_no_hidden_evaluator_read_attempt`: unobservable; diagnostics: Not observable from final workspace files.
- `process_no_network_attempt`: unobservable; diagnostics: AST-visible behavior is audited, but execution history is not observable from final files.
- `writes_only_declared_storage`: unobservable; diagnostics: Final workspace files cannot prove that runtime writes stayed within declared storage.

注：`workspace_non_source` 判 `src/__init__.py` 为边界外 source。该文件与 template 字节一致（hash c127a6d8...），此失败是 audit 规则对 template 自带文件的系统性判定，与 phi_5 及原十模型轮完全相同，不代表候选修改了该文件。

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

- DS1: strict=False (1/2)
  - FAIL DS1-C1 -> closed_loop_v2.evaluator.test_delivery_spool.SpoolPersistenceTests.test_initialize_reopen_and_fail_closed
- DS2: strict=False (2/2)
- DS3: strict=False (2/2)
- DS4: strict=False (2/2)
- DS5: strict=False (2/2)

## Token usage（仅 agent-6 wire）

| 分量 | 值 |
|---|---|
| input_other | 46 |
| input_cache_read | 3,568,044 |
| input_cache_creation | 264,177 |
| input_context_tokens | 3,832,267 |
| output_tokens | 154,715 |
| fresh_tokens | 418,938 |
| inference_tokens | 3,986,982 |
| usage_record_count | 23 |
| token_measurement_status | valid |
| raw_wire_model_match | True（原始 usage 中 expected_model=CC/claude-opus-4-8） |
| 超过 10M soft SLA | no |

## 结论

- 候选自报 completed；机械评测 17/20。
- 未闭环项目：OF1（2 个 criterion 失败）、DS1（DS1-C1 失败）；OF2-OF5、DS2-DS5 全部通过。
- InstructionGate=false 属于 src/__init__.py 系统性判定；严格 milestone 因此计 0，criterion 原始结果保留。
- token 计量有效，约 3.99M inference tokens，未超 10M 软上限。
- 执行链有一次 task.lost 后 resume（同一 agent 上下文），以及三次未产生模型产出的失败派发记录，均如实保留。
- 本报告不构成跨模型排名。
