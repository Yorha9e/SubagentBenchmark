# Reviewer Benchmark Results

本目录归档当前已经完成的 Reviewer / B11 `dependency_layers.py` debug 测试结果。

## 当前覆盖范围

已完成并归档 14 个候选：

- `subtest_1`–`subtest_13`
- `phi_2`

未纳入本归档：

- `subtest_14 / grok/grok-4.5`：因上游 429 rate limit 未完成；没有有效 reviewer 输出。
- `subtest_15 / tx/hy3`：按用户要求取消，未完成且不计入排名。

因此本归档的候选数量仍为 14，不应解释为完整的 15 模型榜单。

## 结果版本

- `results/debug-subagent-v1/`
  - 初始 reviewer 评测结果、运行时信息和原始排行榜。
- `results/debug-subagent-v1-replay-v2/`
  - 外置 evaluator 重放结果。
  - 每个 supplemental criterion 独立运行，避免单项超时污染其他检查。
  - 严格榜和宽松榜均已生成，当前没有未解决并列。

外置 evaluator 重放的结果以 `debug-subagent-v1-replay-v2/leaderboard.md` 和其下的机器可读 JSON 为准。

## 当前严格榜摘要

1. `subtest_7` / `GPT/gpt-5.6-luna`
2. `subtest_4` / `kimi-code/kimi-for-coding`
3. `subtest_6` / `qwen/qwen3.8-max-preview`
4. `subtest_8` / `volcano/doubao-seed-2.1-turbo`
5. `subtest_9` / `volcano/doubao-seed-2.0-pro`
6. `subtest_5` / `stepfun/step-3.7-flash`
7. `phi_2` / `volcano/glm-5.2`
8. `subtest_3` / `deepseek/deepseek-v4-pro`
9. `subtest_12` / `mimo/mimo-v2.5-pro`
10. `subtest_11` / `volcano/minimax-m3`
11. `subtest_13` / `mimo/mimo-v2.5`
12. `subtest_10` / `volcano/doubao-seed-2.0-code`
13. `subtest_2` / `deepseek/deepseek-v4-flash`
14. `subtest_1` / `MT/LongCat-2.0`

详细分数、Gate、官方 criterion、资源检查和补充检查请查看对应 leaderboard 文件。

## 辅助内容

- `protocol/`：B11 任务、公开契约、bug report 和补充检查协议。
- `evaluator/reviewer_evaluator/`：外置 evaluator 源码和 schema。
- 本目录不包含候选 workspace、模型原始对话或 token usage；token usage 在本轮不可用。
