# Reviewer Debug Subagent 排行榜（外置 evaluator 重放）

- Run ID：`debug-subagent-v1-replay-v2`
- 任务：B11 `dependency_layers.py` 初步 Debug
- 候选数量：14（两轮，每轮 7 个）
- evaluator：`reviewer_evaluator`，版本 `reviewer-b11-external-v2`
- 官方评测：复用冻结的 `short/harness/evaluate.py`；未修改 `short/` 或任何候选工作区。
- Token：不可用（没有可信 usage 记录，未估算）。

## 严格确定性榜

排序键：Instruction Gate、官方 criterion 通过数、官方资源通过数、补充检查通过数、补充性能中位数。

| 排名 | 候选 | 模型 | Gate | 官方 criterion | 官方资源 | 补充检查 | 性能中位数 |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `subtest_7` | `GPT/gpt-5.6-luna` | 1 | 16/16 | 2/2 | 8/8 | 151.672 ms |
| 2 | `subtest_4` | `kimi-code/kimi-for-coding` | 1 | 16/16 | 2/2 | 8/8 | 152.541 ms |
| 3 | `subtest_6` | `qwen/qwen3.8-max-preview` | 1 | 16/16 | 2/2 | 7/8 | 112.138 ms |
| 4 | `subtest_8` | `volcano/doubao-seed-2.1-turbo` | 1 | 16/16 | 2/2 | 7/8 | 115.425 ms |
| 5 | `subtest_9` | `volcano/doubao-seed-2.0-pro` | 1 | 16/16 | 2/2 | 7/8 | 116.831 ms |
| 6 | `subtest_5` | `stepfun/step-3.7-flash` | 1 | 16/16 | 2/2 | 7/8 | 117.036 ms |
| 7 | `phi_2` | `volcano/glm-5.2` | 1 | 16/16 | 2/2 | 7/8 | 117.286 ms |
| 8 | `subtest_3` | `deepseek/deepseek-v4-pro` | 1 | 16/16 | 2/2 | 7/8 | 118.536 ms |
| 9 | `subtest_12` | `mimo/mimo-v2.5-pro` | 1 | 16/16 | 2/2 | 7/8 | 119.739 ms |
| 10 | `subtest_11` | `volcano/minimax-m3` | 1 | 16/16 | 2/2 | 7/8 | 121.195 ms |
| 11 | `subtest_13` | `mimo/mimo-v2.5` | 1 | 16/16 | 2/2 | 7/8 | 124.323 ms |
| 12 | `subtest_10` | `volcano/doubao-seed-2.0-code` | 1 | 16/16 | 1/2 | 6/8 | 61.646 ms |
| 13 | `subtest_2` | `deepseek/deepseek-v4-flash` | 1 | 16/16 | 1/2 | 6/8 | 63.297 ms |
| 14 | `subtest_1` | `MT/LongCat-2.0` | 0 | 16/16 | 2/2 | 7/8 | 123.907 ms |

## 宽松确定性榜

宽松榜不把 Instruction Gate 作为排序前置条件，但仍保留 Gate 字段；其余排序键相同。

| 排名 | 候选 | 模型 | Gate | 官方 criterion | 官方资源 | 补充检查 | 性能中位数 |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `subtest_7` | `GPT/gpt-5.6-luna` | 1 | 16/16 | 2/2 | 8/8 | 151.672 ms |
| 2 | `subtest_4` | `kimi-code/kimi-for-coding` | 1 | 16/16 | 2/2 | 8/8 | 152.541 ms |
| 3 | `subtest_6` | `qwen/qwen3.8-max-preview` | 1 | 16/16 | 2/2 | 7/8 | 112.138 ms |
| 4 | `subtest_8` | `volcano/doubao-seed-2.1-turbo` | 1 | 16/16 | 2/2 | 7/8 | 115.425 ms |
| 5 | `subtest_9` | `volcano/doubao-seed-2.0-pro` | 1 | 16/16 | 2/2 | 7/8 | 116.831 ms |
| 6 | `subtest_5` | `stepfun/step-3.7-flash` | 1 | 16/16 | 2/2 | 7/8 | 117.036 ms |
| 7 | `phi_2` | `volcano/glm-5.2` | 1 | 16/16 | 2/2 | 7/8 | 117.286 ms |
| 8 | `subtest_3` | `deepseek/deepseek-v4-pro` | 1 | 16/16 | 2/2 | 7/8 | 118.536 ms |
| 9 | `subtest_12` | `mimo/mimo-v2.5-pro` | 1 | 16/16 | 2/2 | 7/8 | 119.739 ms |
| 10 | `subtest_11` | `volcano/minimax-m3` | 1 | 16/16 | 2/2 | 7/8 | 121.195 ms |
| 11 | `subtest_1` | `MT/LongCat-2.0` | 0 | 16/16 | 2/2 | 7/8 | 123.907 ms |
| 12 | `subtest_13` | `mimo/mimo-v2.5` | 1 | 16/16 | 2/2 | 7/8 | 124.323 ms |
| 13 | `subtest_10` | `volcano/doubao-seed-2.0-code` | 1 | 16/16 | 1/2 | 6/8 | 61.646 ms |
| 14 | `subtest_2` | `deepseek/deepseek-v4-flash` | 1 | 16/16 | 1/2 | 6/8 | 63.297 ms |

## 并列与审核层

- 严格榜未解决并列：无。
- 宽松榜未解决并列：无。
- 未启动 LLM/人工 tie-break；`review-layer.json` 记录为 `not_started`。
- `review-input.json` 记录了空 tie 候选清单；未来审核只能作为 advisory 层，不能改写确定性排名。

## 与旧版结果的差异

旧版 supplemental evaluator 将所有补充检查放在同一个 subprocess 中。`subtest_2` 和 `subtest_10` 的深规模检查超时后，旧版把整套补充结果记成 `0/8`。本版按 criterion 独立启动 subprocess，只记录对应的 `deep_50000` 超时，其他检查仍得到真实结果。

| 候选 | 旧版 supplemental | 新版 supplemental | 新版超时项 |
|---|---:|---:|---|
| `subtest_2` | 0/8（timeout） | 6/8（completed） | `deep_50000` |
| `subtest_10` | 0/8（timeout） | 6/8（completed） | `deep_50000` |

这不是候选代码变好或变坏，而是评测隔离粒度修正：旧版 aggregate timeout 被拆成单项 timeout。

## 结果文件

```text
reviewer/results/debug-subagent-v1-replay-v2/evaluations/
reviewer/results/debug-subagent-v1-replay-v2/deterministic-ranking.json
reviewer/results/debug-subagent-v1-replay-v2/review-input.json
reviewer/results/debug-subagent-v1-replay-v2/review-layer.json
reviewer/results/debug-subagent-v1-replay-v2/comparison.json
```
