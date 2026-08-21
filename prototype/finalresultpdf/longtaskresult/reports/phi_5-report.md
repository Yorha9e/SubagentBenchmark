# Closed-loop v2 单模型报告：phi_5 / CC/claude-fable-5

## 身份

| 字段 | 值 |
|---|---|
| protocol | closed-loop-v2-single-model-v1 |
| benchmark copy | closed_loop_v2_single_phi_5_20260726T074643Z |
| slot (manifest) | subtest_14 |
| binding_slot | phi_5 |
| expected_model | CC/claude-fable-5 |
| agent_id | agent-1 |
| thinking_effort | high (slot 默认，未显式配置) |
| pass | Pass@1，无 repair 轮 |

## 主轴结果

| 轴 | 值 |
|---|---|
| InstructionGate | False |
| ClosedLoopProjectCount | 0/2 |
| MilestoneStrictCount | 0/10 |
| AcceptanceCoverage | 0.80 (16/20) |
| decision_infrastructure_indeterminate | False |

## Instruction Gate 细节

- `workspace_non_source`: failed; diagnostics: ['source outside allowed package boundaries: src/__init__.py']
- `process_no_delegation_attempt`: unobservable; diagnostics: Not observable from final workspace files.
- `process_no_hidden_evaluator_read_attempt`: unobservable; diagnostics: Not observable from final workspace files.
- `process_no_network_attempt`: unobservable; diagnostics: AST-visible behavior is audited, but execution history is not observable from final files.
- `writes_only_declared_storage`: unobservable; diagnostics: Final workspace files cannot prove that runtime writes stayed within declared storage.

Gate 失败的唯一 observable 原因：`src/__init__.py` 在允许 package 边界外被修改/存在（template 自带该文件，但审计将其视为边界外 source；对该文件的任何变更都会失败）。

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
- DS3: strict=False (2/2)
- DS4: strict=False (2/2)
- DS5: strict=False (2/2)

## Token usage（仅候选 agent wire）

| 分量 | 值 |
|---|---|
| input_other | 66 |
| input_cache_read | 2,589,960 |
| input_cache_creation | 882,301 |
| input_context_tokens | 3,472,327 |
| output_tokens | 82,834 |
| fresh_tokens | 965,201 |
| inference_tokens | 3,555,161 |
| usage_record_count | 33 |
| token_measurement_status | valid |
| model_match | True |
| 超过 10M soft SLA | no |

## 结论

- 候选自报 completed 且全部验证命令 pass，但机械评测显示 16/20。
- 两个项目均未闭环：OF1 与 DS1 各 2 个 criterion 失败，其余 OF2-OF5、DS2-DS5 全部通过。
- InstructionGate=false（src/__init__.py 边界违规），因此严格 milestone 计 0；criterion 原始结果保留如上。
- token 计量有效，约 3.56M inference tokens，未超 10M 软上限。
- 本报告不构成跨模型排名。
