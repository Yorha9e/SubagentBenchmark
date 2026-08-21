# Critic / Reviewer results archive

本目录归档项目中已有的 Critic、Reviewer Debug 和 Critic pilot 结果，以及对应的可复核输入、运行产物和 evaluator。归档通过复制生成，不修改来源数据。

## 归档范围

### `results/critic-model-select-v1/`

正式 Critic 模型选型实验：

- 15 个 Critic 候选：`subtest_1`–`subtest_14` + `phi_2`
- 包含后续补充的 `subtest_14 / grok/grok-4.5` high-effort 成功 A/B 重跑
- 保留原 Provider 400 失败事件、timing metadata、reviews、score summary、leaderboard 和 candidate inputs
- 最终 score summary 为 15 个 scored candidates

主要文件：

- `critic-leaderboard.md`
- `total-leaderboard.md`
- `leaderboard.md`
- `score-summary.json`
- `timing-events.json`
- `SCORING.md`
- `manifest.json`
- `reviews/*.json`

### `results/debug-subagent-v1/`

B11 `dependency_layers.py` 初步 Debug 的 14 个模型结果，包含两轮 evaluation、排行榜、补充检查和运行时摘要。

### `results/debug-subagent-v1-replay-v2/`

使用外置 `reviewer_evaluator` 的确定性 replay 结果，包含严格/宽松榜、逐模型 evaluation、comparison 和 review layer 记录。

### `results/debug-subagent-v1-critic-v1/`

3 个盲化候选的 Critic pilot，包含 raw review JSON、结构化 review、finding summary、timing summary 和候选输入。

## 其他归档内容

- `runs/debug-subagent-v1/`：B11 Debug 两轮候选 workspace 和运行证据。
- `evaluator/reviewer_evaluator/`：外置 reviewer evaluator 及其 schema/checks。
- `protocol/`：Debug 任务说明、公共 smoke、补充检查、B11 bug report、共享计划和任务协议。

## 重要边界

- 这是 Critic/Reviewer 结果归档，不是 short benchmark 模型完成度总榜；不要将本目录的分数与 `shorttaskresult/` 直接合并。
- 当前 Critic 选型正式结果补充到 `subtest_14 / grok/grok-4.5`；后续 short A17/B17 的 `subtest_15 / tx/hy3` 尚未进行 Critic 选型测试，因此没有伪装加入本归档。
- `subtest_14` 的 high-effort 成功结果与此前 Provider 失败均保留，失败事件不覆盖成功结果。
- `.pyc`、`__pycache__`、cache、failed-cell 证据和 timing metadata 均按来源原样保留，以便复核。
- `debug-subagent-v1-critic-v1` 中部分前台 Agent 原始输出没有单独持久化文件；对应的结构化 raw JSON、timing summary 和 finding summary 是当前可复核记录。

## 完整性

`archive-manifest.json` 记录归档时间、来源根目录、相对路径、字节数和 SHA-256。其 `files` 数组覆盖除自身外的全部归档文件。
