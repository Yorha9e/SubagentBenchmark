# Short benchmark A/B 模型总表（spec-conformant-v2）

> 评分规则：`spec-conformant-v2`。候选代码和 token 数据未修改，仅修订 evaluator 的公开契约一致性。严格排名优先考虑 Instruction Gate、完整任务数、official criteria、扩展能力、资源能力和 token 效率。

## A 条件总表（仅 `TASKS.md`）

| 严格排名 | 宽松排名 | Slot | 模型 | Gate | Tasks | Official | Raw | Ext | Res | Tokens | 失败 criterion |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1 | A07 | GPT/gpt-5.6-luna | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 306,032 | — |
| 2 | 2 | A14 | volcano/glm-5.2 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 426,426 | — |
| 3 | 3 | A06 | qwen/qwen3.8-max-preview | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 561,153 | — |
| 4 | 4 | A04 | kimi-code/kimi-for-coding | 1 | 4/4 | 16/16 | 16/16 | 1/2 | 2/2 | 194,101 | — |
| 5 | 5 | A03 | deepseek/deepseek-v4-pro | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 340,599 | `ttl_strict_types` |
| 6 | 6 | A08 | volcano/doubao-seed-2.1-turbo | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 729,724 | `rp_plain_dict` |
| 7 | 7 | A01 | MT/LongCat-2.0 | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 1/2 | 1,050,748 | `rp_plain_dict` |
| 8 | 8 | A09 | volcano/doubao-seed-2.0-pro | 1 | 3/4 | 15/16 | 15/16 | 1/2 | 2/2 | 223,366 | `rp_isolation` |
| 9 | 10 | A11 | volcano/minimax-m3 | 1 | 3/4 | 14/16 | 14/16 | 2/2 | 1/2 | 1,253,213 | `rp_plain_dict`, `rp_isolation` |
| 10 | 9 | A12 | mimo/mimo-v2.5-pro | 1 | 2/4 | 14/16 | 14/16 | 2/2 | 2/2 | 419,022 | `rp_plain_dict`, `ttl_gc_release` |
| 11 | 11 | A15 | composer/composer-2.5 † | 1 | 2/4 | 14/16 | 14/16 | 1/2 | 1/2 | N/A | `rp_plain_dict`, `ttl_strict_types` |
| 12 | 13 | A02 | deepseek/deepseek-v4-flash | 1 | 2/4 | 13/16 | 13/16 | 2/2 | 1/2 | 254,003 | `dl_deep_iterative`, `ttl_strict_types`, `ttl_gc_release` |
| 13 | 12 | A13 | mimo/mimo-v2.5 | 1 | 2/4 | 13/16 | 13/16 | 0/2 | 2/2 | 184,589 | `rp_isolation`, `du_units_ranges`, `du_normalize` |
| 14 | 13 | A05 | stepfun/step-3.7-flash | 1 | 1/4 | 12/16 | 12/16 | 2/2 | 1/2 | 591,861 | `rp_plain_dict`, `ttl_strict_types`, `ttl_gc_release`, `du_structured_errors` |
| 15 | 14 | A10 | volcano/doubao-seed-2.0-code | 1 | 1/4 | 12/16 | 12/16 | 1/2 | 1/2 | 379,863 | `rp_isolation`, `dl_deep_iterative`, `ttl_strict_types`, `ttl_gc_release` |

## B 条件总表（额外读取 phi_3 计划）

| 严格排名 | 宽松排名 | Slot | 模型 | Gate | Tasks | Official | Raw | Ext | Res | Tokens | 失败 criterion / Gate 原因 |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 2 | B13 | mimo/mimo-v2.5 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 342,149 | — |
| 2 | 3 | B08 | volcano/doubao-seed-2.1-turbo | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 602,565 | — |
| 3 | 4 | B14 | volcano/glm-5.2 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 624,991 | — |
| 4 | 5 | B04 | kimi-code/kimi-for-coding | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 803,531 | — |
| 5 | 6 | B06 | qwen/qwen3.8-max-preview | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 863,422 | — |
| 6 | 7 | B01 | MT/LongCat-2.0 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 869,279 | — |
| 7 | 8 | B07 | GPT/gpt-5.6-luna | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 880,477 | — |
| 8 | 9 | B02 | deepseek/deepseek-v4-flash | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 900,470 | — |
| 9 | 1 | B05 | stepfun/step-3.7-flash | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | 326,756 | — |
| 10 | 10 | B03 | deepseek/deepseek-v4-pro | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | 1,407,484 | — |
| 11 | 11 | B15 | composer/composer-2.5 † | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | N/A | — |
| 12 | 12 | B09 | volcano/doubao-seed-2.0-pro | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 276,081 | `ttl_strict_types` |
| 13 | 14 | B10 | volcano/doubao-seed-2.0-code | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 1/2 | 469,287 | `dl_deep_iterative` |
| 14 | 13 | B11 | volcano/minimax-m3 | 1 | 3/4 | 12/16 | 12/16 | 2/2 | 1/2 | 647,000 | 全部 4 个 dependency criteria |
| 15 | 12 | B12 | mimo/mimo-v2.5-pro | 0 | 0/4 | 0/16 | **15/16** | 2/2 | 2/2 | 190,320 | raw 仅失败 `ttl_strict_types`；Gate: `.pytest_cache` |

> B12 的代码 raw 为 15/16，但 `.pytest_cache` 触发 Instruction Gate，严格 Tasks/Official 因此清零。

## 汇总结论

- A 条件第一：`GPT/gpt-5.6-luna`。
- B 条件第一：`mimo/mimo-v2.5`。
- B 条件宽松榜第一：`stepfun/step-3.7-flash`，但资源探针只有 1/2，因此严格榜为第 9。
- 最稳定的跨条件模型：`volcano/glm-5.2`，A/B 都是 16/16，严格排名分别为第 2、第 3。
- phi_3 计划对 8/14 模型提高 raw criteria，5/14 不变，1/14 下降；中位增益为 +1。
- 作为“强模型规划、弱模型执行”的本轮首选：`mimo/mimo-v2.5`。

## 关联文件

- 完整双榜：`final-leaderboard-spec-conformant-v2.md`
- 契约审计：`spec-conformance-audit-v2.md`
- 机器可读报告：`final-report-spec-conformant-v2.json`
- 30 个单元结果：`formal-spec-conformant-v2/`
