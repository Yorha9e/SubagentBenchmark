# Closed-loop v2 单模型报告：subtest_15 / tx/hy3 (max)

## 身份

| 字段 | 值 |
|---|---|
| protocol | closed-loop-v2-single-model-v1 |
| benchmark copy | closed_loop_v2_single_subtest_15_hy3_20260726T143000Z |
| slot (display) | subtest_15 |
| evaluator slot | subtest_1（harness manifest 未登记 subtest_15；criteria identical，结果按 subtest_15 归档） |
| binding_slot | subtest_15 |
| expected_model | tx/hy3 |
| thinking_effort | max（显式配置） |
| agent_id | agent-17 |
| language constraint | English-only prompt/response |
| pass | Pass@1（本 workspace 无 repair 轮） |

## 主轴结果

| 轴 | 值 |
|---|---|
| InstructionGate | False |
| ClosedLoopProjectCount | 0/2 |
| MilestoneStrictCount | 0/10 |
| RawMilestoneCount | 2/10 |
| AcceptanceCoverage | 0.30 (6/20) |
| decision_infrastructure_indeterminate | False |

## Instruction Gate 细节

- `workspace_non_source`: failed; diagnostics: `source outside allowed package boundaries: src/__init__.py`
- 其余可观察结构检查通过或不可观察。
- `src/__init__.py` 为 template 自带文件；该 Gate 失败与此前 closed-loop-v2 单模型运行中的系统性 audit 判定一致，不代表候选修改了该文件。

## Milestone / criterion

### order_fulfillment (closed_loop_success=False)

- OF1: strict=False (0/2)
  - FAIL OF1-C1 -> `test_schema_initialize_and_reopen`
  - FAIL OF1-C2 -> `test_input_and_dependency_validation`
- OF2: strict=True raw (2/2)
- OF3: strict=False (1/2)
  - FAIL OF3-C1 -> payment/idempotency/conflict criterion
- OF4: strict=True raw (2/2)
- OF5: strict=False (1/2)
  - FAIL OF5-C2 -> order CLI protocol/error/persistence criterion

### delivery_spool (closed_loop_success=False)

- DS1: strict=False (0/2)
  - FAIL DS1-C1 -> initialization/reopen/fail-closed criterion
  - FAIL DS1-C2 -> canonical payload/idempotency/limits criterion
- DS2: strict=False (0/2)
  - FAIL DS2-C1
  - FAIL DS2-C2
- DS3: strict=False (0/2)
  - FAIL DS3-C1
  - FAIL DS3-C2
- DS4: strict=False (0/2)
  - FAIL DS4-C1
  - FAIL DS4-C2
- DS5: strict=False (0/2)
  - FAIL DS5-C1
  - FAIL DS5-C2

## Token usage（仅 agent-17 wire）

| 分量 | 值 |
|---|---:|
| input_other | 5,084,309 |
| input_cache_read | 0 |
| input_cache_creation | 0 |
| input_context_tokens | 0 |
| output_tokens | 51,388 |
| fresh_tokens | 5,135,697 |
| inference_tokens | 5,135,697 |
| usage_record_count | 74 |
| token_measurement_status | valid |
| model_match | True |
| 超过 10M soft SLA | no |

## 结论

- 候选自报 completed；机械评测 6/20，RawMilestoneCount=2/10。
- `order_fulfillment` 有部分高层行为通过（OF2、OF4 全过），但基础持久化/依赖校验、部分支付/CLI 仍失败。
- `delivery_spool` 全部 milestone 均未 raw strict 闭环。
- InstructionGate=false 主要来自 template 自带 `src/__init__.py` 的系统性 audit 判定；严格榜应放入未排名区。
- token 计量有效，约 5.14M inference tokens，未超 10M 软上限。
