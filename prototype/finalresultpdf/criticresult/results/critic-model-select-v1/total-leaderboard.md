# Critic Model Selection 总榜

实验：`critic-model-select-v1`  
评分：Recall 50 + Precision 20 + Depth 15 + Speed 10 + Format 5 = 100 分

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

## 说明

- `GT1`：candidate-A 跨 hashability 等值去重缺陷。
- `GT2`：candidate-A unhashable 注册表 `O(N²)` 缺陷。
- `GT3`：candidate-B 跨注册表扫描 `O(N²)` 缺陷。
- Speed 按 14 个有完整 Agent metadata 的模型重新计算；`subtest_3` 使用前台 Agent，计时不可用。
- `subtest_14` 使用 high effort 重跑成功；此前 Provider 失败事件仍保存在 `timing-events.json`，但不影响当前评分。
- token 用量在当前工具层不可见，因此未纳入分数。
