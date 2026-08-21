# Critic 榜单

实验：`critic-model-select-v1`  
目标：比较不同模型作为代码审查 Critic 的缺陷发现能力、准确性、深度、速度和输出契约遵循情况。

## 完整排名

| 排名 | Critic | 模型 | Recall | Precision | Depth | Speed | Format | 总分 | GT 命中 | A/B 总耗时(s) |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | `subtest_4` | `kimi-code/kimi-for-coding` | 50 | 20 | 15 | 2.308 | 5 | **92.308** | GT1, GT2, GT3 | 1331.686 |
| 2 | `subtest_9` | `volcano/doubao-seed-2.0-pro` | 40 | 20 | 15 | 10 | 5 | **90.000** | GT1, GT3 | 68.364 |
| 3 | `subtest_6` | `qwen/qwen3.8-max-preview` | 40 | 20 | 15 | 8.462 | 5 | **88.462** | GT1, GT3 | 342.068 |
| 4 | `subtest_7` | `GPT/gpt-5.6-luna` | 30 | 20 | 12 | 7.692 | 5 | **74.692** | GT1 | 345.965 |
| 5 | `subtest_5` | `stepfun/step-3.7-flash` | 30 | 20 | 12 | 3.846 | 3.5 | **69.346** | GT1 | 560.693 |
| 6 | `subtest_10` | `volcano/doubao-seed-2.0-code` | 30 | 20 | 8 | 9.231 | 2 | **69.231** | GT1 | 216.314 |
| 7 | `subtest_8` | `volcano/doubao-seed-2.1-turbo` | 30 | 20 | 8 | 3.077 | 3.5 | **64.577** | GT1 | 644.110 |
| 8 | `subtest_12` | `mimo/mimo-v2.5-pro` | 30 | 20 | 8 | 1.538 | 3.5 | **63.038** | GT1 | 2126.660 |
| 9 | `subtest_1` | `MT/LongCat-2.0` | 10 | 20 | 15 | 0.769 | 2 | **47.769** | GT2 | 2734.619 |
| 10 | `subtest_2` | `deepseek/deepseek-v4-flash` | 0 | 20 | 0 | 6.923 | 2 | **28.923** | — | 428.043 |
| 11 | `phi_2` | `volcano/glm-5.2` | 0 | 20 | 1 | 5.385 | 2 | **28.385** | — | 485.288 |
| 12 | `subtest_11` | `volcano/minimax-m3` | 0 | 20 | 0 | 6.154 | 2 | **28.154** | — | 430.697 |
| 13 | `subtest_13` | `mimo/mimo-v2.5` | 0 | 20 | 1 | 4.615 | 2 | **27.615** | — | 520.938 |
| 14 | `subtest_14` | `grok/grok-4.5` | 0 | 20 | 0 | 0 | 2 | **22.000** | — | 3027.971 |
| 15 | `subtest_3` | `deepseek/deepseek-v4-pro` | 0 | 15 | 0 | 0 | 0 | **15.000** | — | unavailable |

## 评分维度

- **Recall：50 分** — GT1、GT2、GT3 缺陷召回。
- **Precision：20 分** — 误报纪律；每个确认误报扣 5 分。
- **Depth：15 分** — finding 根因和影响分析深度。
- **Speed：10 分** — A/B 两次 Agent metadata 墙钟耗时排名。
- **Format：5 分** — 严格 JSON、可解析性和字段完整性。

## 关键结论

### 最强缺陷发现能力

`subtest_4 / kimi-for-coding` 获得 **92.308 分**，唯一同时命中 GT1、GT2、GT3，适合用于高召回代码审查和资源问题发现。

### 最佳速度和性价比

`subtest_9 / doubao-seed-2.0-pro` 仅用 **68.364 秒**完成 A/B 审查，命中 GT1、GT3，适合作为需要快速反馈的默认 Critic。

### 最佳综合平衡

`subtest_6 / qwen3.8-max-preview` 获得 **88.462 分**，命中 GT1、GT3，并保持较好的深度、格式和速度表现。

### subtest_14 结果

`grok/grok-4.5` 在 high effort 重跑后成功完成 A/B，但两侧均未发现预设 GT 缺陷，且总耗时 `3027.971` 秒，因此排名第 14。此前 Provider 400 失败事件保存在 `timing-events.json`，不影响本次 high-effort 结果。

## 数据文件

- 评分明细：`score-summary.json`
- 原始计时：`timing-events.json`
- 单模型审查：`reviews/*.json`
- 评分协议：`SCORING.md`
