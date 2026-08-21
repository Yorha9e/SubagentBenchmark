# 短任务测试报告：doubao-seed-evolving

## 测试信息

- 模型：`volcanoagent/doubao-seed-evolving`（slot `subtest1`，thinking_effort `high`）
- Benchmark：`short-python-stdlib-v1`
- 测试日期：2026-07-27
- 隔离目录：`shorttaskresult/doubao-evolving/`

## A/B 评测结果

| 维度 | A 条件（仅 TASKS.md） | B 条件（+frozen-phi3-plan.md） |
|---|---|---|
| Instruction Gate | ✓ 通过 | ✓ 通过 |
| Official criteria | **16/16** | **16/16** |
| Extension | **2/2** | **2/2** |
| Resource | **2/2** | **1/2**（res_dependency_20000 超时） |
| Strict tasks | **4/4** | **4/4** |
| Raw criteria | 16/16 | 16/16 |
| 执行耗时 | 466.4s | 320.9s |
| Token usage | N/A | N/A |

## A 条件详细

全部 16 个 criterion 通过，2 个扩展测试通过，2 个资源测试通过。Gate 通过。

这是 A 条件的**最高分**，与 glm-5.2、qwen3.8、grok-4.5 并列（排除 gpt）。

## B 条件详细

全部 16 个 criterion 通过，2 个扩展测试通过。Gate 通过。

唯一失败项：`res_dependency_20000`（20,000 节点性能测试）超时。其余全部通过。

A 条件通过了同一个资源测试，说明 B 条件的 `dependency_layers.py` 实现可能遵循计划但采用了不同的（较慢的）算法路径。

## 与现有短任务榜对比（排除 gpt/cc）

### A 条件严格榜

| 排名 | 模型 | Official | Ext | Res | Tokens |
|---:|---|---:|---:|---:|---:|
| 1 | `glm-5.2` | 16/16 | 2/2 | 2/2 | 426k |
| 2 | `qwen3.8` | 16/16 | 2/2 | 2/2 | 561k |
| 3 | `grok-4.5` | 16/16 | 2/2 | 2/2 | N/A |
| **4** | **`doubao-seed-evolving`** | **16/16** | **2/2** | **2/2** | **N/A** |
| 5 | `kimi-for-coding` | 16/16 | 1/2 | 2/2 | 194k |
| 6 | `deepseek-v4-pro` | 15/16 | 2/2 | 2/2 | 341k |

doubao-seed-evolving A 条件并列第 1，与 glm-5.2、qwen3.8、grok-4.5 同为满分。

### B 条件严格榜

| 排名 | 模型 | Official | Ext | Res | Tokens |
|---:|---|---:|---:|---:|---:|
| 1 | `mimo-v2.5` | 16/16 | 2/2 | 2/2 | 342k |
| 2 | `doubao-seed-2.1-turbo` | 16/16 | 2/2 | 2/2 | 603k |
| 3 | `glm-5.2` | 16/16 | 2/2 | 2/2 | 625k |
| 4 | `kimi-for-coding` | 16/16 | 2/2 | 2/2 | 804k |
| 5 | `qwen3.8` | 16/16 | 2/2 | 2/2 | 863k |
| 6 | `LongCat-2.0` | 16/16 | 2/2 | 2/2 | 869k |
| 7 | `deepseek-v4-flash` | 16/16 | 2/2 | 2/2 | 900k |
| 8 | `step-3.7-flash` | 16/16 | 2/2 | 1/2 | 327k |
| **9** | **`doubao-seed-evolving`** | **16/16** | **2/2** | **1/2** | **N/A** |

B 条件因 `res_dependency_20000` 超时排在 res 2/2 模型之后，与 step-3.7-flash 同档（res 1/2）。

## A/B Delta

| 指标 | A -> B | 变化 |
|---|---|---|
| Raw criteria | 16 -> 16 | 持平 |
| Resource | 2/2 -> 1/2 | 退步（超时） |
| Extension | 2/2 -> 2/2 | 持平 |
| Gate | ✓ -> ✓ | 持平 |
| 耗时 | 466s -> 321s | B 更快 |

## 关键结论

1. **A 条件满分**：代码完成度与 glm-5.2、qwen3.8 持平，全中 16 criterion + 2 ext + 2 res。
2. **B 条件仅 res 超时**：代码正确性满分（16/16），但 20,000 节点性能测试超时。可能是 B 条件读了计划后采用了不同的实现策略。
3. **A 通过但 B 超时**：说明模型在 A 条件下自己选择的算法反而比读计划后实现的版本更高效。
4. **执行速度**：A 466s、B 321s，在短任务中属于中等偏快（比 LongCat-2.0 的 1100s+ 快，比 step-3.7-flash 的 120s 慢）。
5. **Token 不可用**：后台任务无 usage 数据。

## 综合评价

doubao-seed-evolving 在短任务（coder 角色）中表现**顶级**：A 条件满分，B 条件仅差一个资源测试。结合 critic 测试中全中 3 GT 的表现，这是一个**coder 和 critic 双强**的模型。

| 角色 | 排名 | 关键指标 |
|---|---|---|
| Coder (A 条件) | 并列第 1（排除 gpt） | 16/16 + ext 2/2 + res 2/2 |
| Coder (B 条件) | 第 9（排除 gpt） | 16/16 + ext 2/2 + res 1/2 |
| Critic | 第 2（排除 gpt） | GT1/2/3 全中 + 0 误报 |

## 文件清单

```
runs/prepared/A/A01/          # A 条件 workspace（含 4 个 solution 文件）
runs/prepared/B/B01/          # B 条件 workspace（含 4 个 solution 文件）
results/A01.json              # A 条件评测结果
results/B01.json              # B 条件评测结果
results/report.md             # 本文件
```
