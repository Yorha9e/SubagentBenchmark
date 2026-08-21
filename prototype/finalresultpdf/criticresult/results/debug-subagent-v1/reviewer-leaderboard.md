# Reviewer Debug Subagent 排行榜

## 测试批次

- Run ID：`debug-subagent-v1`
- 任务：B11 `dependency_layers.py` 初步 Debug
- 第一轮：`subtest_1`—`subtest_7`
- 第二轮：`subtest_8`—`subtest_13`、`phi_2`
- 候选数量：14
- 原始缺陷基线：`short/runs/prepared/B/B11`
- `dependency_layers.py` 基线 SHA-256：`b2fd2e1bad815f358df1d994544d6c775c66765e8f33610fc1e7cb3052a67874`
- evaluator：`short/evaluator` + `short/harness/evaluate.py`

## 排行榜

| 排名 | 候选 | 模型 | 官方功能 | 资源测试 | 补充边界 | Instruction Gate |
|---:|---|---|---:|---|---:|---|
| 1 | `subtest_7` | `GPT/gpt-5.6-luna` | 16/16 | 通过 | 8/8 | 通过 |
| 2 | `subtest_4` | `kimi-code/kimi-for-coding` | 16/16 | 通过 | 8/8 | 通过 |
| 3 | `phi_2` | `volcano/glm-5.2` | 16/16 | 通过 | 7/8 | 通过 |
| 4 | `subtest_6` | `qwen/qwen3.8-max-preview` | 16/16 | 通过 | 7/8 | 通过 |
| 5 | `subtest_5` | `stepfun/step-3.7-flash` | 16/16 | 通过 | 7/8 | 通过 |
| 6 | `subtest_12` | `mimo/mimo-v2.5-pro` | 16/16 | 通过 | 7/8 | 通过 |
| 7 | `subtest_8` | `volcano/doubao-seed-2.1-turbo` | 16/16 | 通过 | 7/8 | 通过 |
| 8 | `subtest_9` | `volcano/doubao-seed-2.0-pro` | 16/16 | 通过 | 7/8 | 通过 |
| 9 | `subtest_11` | `volcano/minimax-m3` | 16/16 | 通过 | 7/8 | 通过 |
| 10 | `subtest_13` | `mimo/mimo-v2.5` | 16/16 | 通过 | 7/8 | 通过 |
| 11 | `subtest_3` | `deepseek/deepseek-v4-pro` | 16/16 | 通过 | 7/8 | 通过 |
| 12 | `subtest_10` | `volcano/doubao-seed-2.0-code` | 16/16 | 超时 | 超时 | 通过 |
| 13 | `subtest_2` | `deepseek/deepseek-v4-flash` | 16/16 | 超时 | 超时 | 通过 |
| 14 | `subtest_1` | `MT/LongCat-2.0` | 16/16 | 通过 | 7/8 | 失败 |

## 排名口径

排序优先级为：

1. `InstructionGate`
2. `dependency_layers` 官方 criterion 通过数
3. `res_dependency_20000` 资源测试
4. 官方 raw criterion 总数
5. 补充业务边界测试
6. 代码完成性、边界处理、复杂度和资源管理复核

不把注释数量、文字风格和一般可读性作为主要评分依据。

## 关键结论

### 第一名：`subtest_7` / `GPT/gpt-5.6-luna`

- 官方 criterion：`16/16`
- 资源测试：通过
- 补充边界：`8/8`
- Instruction Gate：通过
- 正确处理了可哈希与不可哈希节点之间的等值注册。
- 在本次 B11 初步 Debug 任务中综合完成度最高。

### 第二名：`subtest_4` / `kimi-code/kimi-for-coding`

- 官方 criterion：`16/16`
- 资源测试：通过
- 补充边界：`8/8`
- Instruction Gate：通过
- 功能边界完整，但使用用户对象作为字典键，面对异常 equality 或状态化 equality 时的资源和副作用风险高于 `subtest_7`。

### 第三名：`phi_2` / `volcano/glm-5.2`

- 官方 criterion：`16/16`
- 资源测试：通过
- 补充边界：`7/8`
- Instruction Gate：通过
- 使用线性复杂度的层分配方案，补充性能测试中表现最好。
- 失败项为跨哈希性节点等值边界。

### 降级候选

- `subtest_10` 和 `subtest_2` 的功能 criterion 全部通过，但仍采用 O(V²) 的剩余节点扫描，20,000 节点资源测试超时。
- `subtest_1` 的代码行为和性能均通过，但额外创建了 `test_targeted.py`，违反工作区交付约束，导致 Instruction Gate 失败。

## 结果文件

完整机器可读结果：

```text
reviewer/results/debug-subagent-v1/summary.json
reviewer/results/debug-subagent-v1/evaluations/
reviewer/results/debug-subagent-v1/supplemental-results.json
```

本次测试没有可用的 `events.jsonl` 或 `usage.json`，因此 token 消耗未纳入排序，记录为 unavailable。
