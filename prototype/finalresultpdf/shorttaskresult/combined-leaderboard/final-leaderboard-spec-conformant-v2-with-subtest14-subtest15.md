# Short benchmark 总榜（spec-conformant-v2 + subtest_14 + subtest_15 supplemental）

## 说明

本文件在原 15 模型 `spec-conformant-v2` 总榜基础上，追加两个隔离 supplemental 结果：

- A16/B16：`subtest_14`，`grok/grok-4.5`，high effort。
- A17/B17：`subtest_15`，`tx/hy3`，max effort，所有 subagent prompt 均为英文。

原冻结榜 `short/results/final-leaderboard-spec-conformant-v2.md` 未覆盖。

标记：`†` = Composer Cursor harness；`‡` = subtest_14 supplemental；`§` = subtest_15 English-prompt supplemental。

## 插入后结论

- A17 `tx/hy3`：严格榜第 12 / 17；宽松榜第 12 / 17。
- B17 `tx/hy3`：严格榜第 16 / 17；宽松榜第 13 / 17。
- B17 raw 为 16/16，但因 `.pytest_cache` 触发 Instruction Gate，严格分清零；不能 posthoc 删除缓存后冒充原始单次结果。
- A17 raw/official 为 14/16，失败 `rp_isolation` 与 `ttl_strict_types`。

## A 条件（仅 TASKS.md）

| 严格排名 | 宽松排名 | Slot | 模型 | Gate | Tasks | Official | Raw | Ext | Res | Tokens | 失败 criterion / Gate 原因 |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1 | A07 | `GPT/gpt-5.6-luna` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 306,032 | — |
| 2 | 2 | A14 | `volcano/glm-5.2` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 426,426 | — |
| 3 | 3 | A06 | `qwen/qwen3.8-max-preview` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 561,153 | — |
| 4 | 4 | A16 | `grok/grok-4.5` ‡ | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | N/A | — |
| 5 | 5 | A04 | `kimi-code/kimi-for-coding` | 1 | 4/4 | 16/16 | 16/16 | 1/2 | 2/2 | 194,101 | — |
| 6 | 6 | A03 | `deepseek/deepseek-v4-pro` | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 340,599 | `ttl_strict_types` |
| 7 | 7 | A08 | `volcano/doubao-seed-2.1-turbo` | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 729,724 | `rp_plain_dict` |
| 8 | 8 | A01 | `MT/LongCat-2.0` | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 1/2 | 1,050,748 | `rp_plain_dict` |
| 9 | 9 | A09 | `volcano/doubao-seed-2.0-pro` | 1 | 3/4 | 15/16 | 15/16 | 1/2 | 2/2 | 223,366 | `rp_isolation` |
| 10 | 11 | A11 | `volcano/minimax-m3` | 1 | 3/4 | 14/16 | 14/16 | 2/2 | 1/2 | 1,253,213 | `rp_plain_dict`, `rp_isolation` |
| 11 | 10 | A12 | `mimo/mimo-v2.5-pro` | 1 | 2/4 | 14/16 | 14/16 | 2/2 | 2/2 | 419,022 | `rp_plain_dict`, `ttl_gc_release` |
| 12 | 12 | A17 | `tx/hy3` § | 1 | 2/4 | 14/16 | 14/16 | 2/2 | 2/2 | N/A | `rp_isolation`, `ttl_strict_types` |
| 13 | 13 | A15 | `composer/composer-2.5` † | 1 | 2/4 | 14/16 | 14/16 | 1/2 | 1/2 | N/A | `rp_plain_dict`, `ttl_strict_types` |
| 14 | 16 | A02 | `deepseek/deepseek-v4-flash` | 1 | 2/4 | 13/16 | 13/16 | 2/2 | 1/2 | 254,003 | `dl_deep_iterative`, `ttl_strict_types`, `ttl_gc_release` |
| 15 | 14 | A13 | `mimo/mimo-v2.5` | 1 | 2/4 | 13/16 | 13/16 | 0/2 | 2/2 | 184,589 | `rp_isolation`, `du_units_ranges`, `du_normalize` |
| 16 | 15 | A05 | `stepfun/step-3.7-flash` | 1 | 1/4 | 12/16 | 12/16 | 2/2 | 1/2 | 591,861 | `rp_plain_dict`, `ttl_strict_types`, `ttl_gc_release`, `du_structured_errors` |
| 17 | 17 | A10 | `volcano/doubao-seed-2.0-code` | 1 | 1/4 | 12/16 | 12/16 | 1/2 | 1/2 | 379,863 | `rp_isolation`, `dl_deep_iterative`, `ttl_strict_types`, `ttl_gc_release` |

## B 条件（额外读取 phi_3 计划）

| 严格排名 | 宽松排名 | Slot | 模型 | Gate | Tasks | Official | Raw | Ext | Res | Tokens | 失败 criterion / Gate 原因 |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 2 | B13 | `mimo/mimo-v2.5` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 342,149 | — |
| 2 | 3 | B08 | `volcano/doubao-seed-2.1-turbo` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 602,565 | — |
| 3 | 4 | B14 | `volcano/glm-5.2` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 624,991 | — |
| 4 | 5 | B04 | `kimi-code/kimi-for-coding` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 803,531 | — |
| 5 | 6 | B06 | `qwen/qwen3.8-max-preview` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 863,422 | — |
| 6 | 7 | B01 | `MT/LongCat-2.0` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 869,279 | — |
| 7 | 8 | B07 | `GPT/gpt-5.6-luna` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 880,477 | — |
| 8 | 9 | B02 | `deepseek/deepseek-v4-flash` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 900,470 | — |
| 9 | 11 | B16 | `grok/grok-4.5` ‡ | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | N/A | — |
| 10 | 1 | B05 | `stepfun/step-3.7-flash` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | 326,756 | — |
| 11 | 10 | B03 | `deepseek/deepseek-v4-pro` | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | 1,407,484 | — |
| 12 | 11 | B15 | `composer/composer-2.5` † | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | N/A | — |
| 13 | 14 | B09 | `volcano/doubao-seed-2.0-pro` | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 276,081 | `ttl_strict_types` |
| 14 | 17 | B10 | `volcano/doubao-seed-2.0-code` | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 1/2 | 469,287 | `dl_deep_iterative` |
| 15 | 16 | B11 | `volcano/minimax-m3` | 1 | 3/4 | 12/16 | 12/16 | 2/2 | 1/2 | 647,000 | `dl_one_shot`, `dl_dependency_nodes`, `dl_stable_order_cycle`, `dl_deep_iterative` |
| 16 | 15 | B12 | `mimo/mimo-v2.5-pro` | 0 | 0/4 | 0/16 | 15/16 | 2/2 | 2/2 | 190,320 | `ttl_strict_types`; Gate: unexpected workspace entry .pytest_cache |
| 16 | 13 | B17 | `tx/hy3` § | 0 | 0/4 | 0/16 | 16/16 | 2/2 | 2/2 | N/A | Gate: unexpected workspace entry .pytest_cache |

## supplemental A/B delta

| 模型 | A → B | Raw Δ | Strict task Δ | Gate Δ | Token Δ |
|---|---|---:|---:|---:|---:|
| `grok/grok-4.5` ‡ | A16 → B16 | +0 | +0 | +0 | N/A |
| `tx/hy3` § | A17 → B17 | +2 | -2 | -1 | N/A |

## 关联文件

- 机器可读扩展报告：`short/results/final-report-spec-conformant-v2-with-subtest14-subtest15.json`
- subtest_15 隔离报告：`short_subtest15_english/results/subtest15-english-report.md`
- subtest_14 隔离报告：`short_subtest14_grok_high/results/subtest14-grok-high-report.md`
