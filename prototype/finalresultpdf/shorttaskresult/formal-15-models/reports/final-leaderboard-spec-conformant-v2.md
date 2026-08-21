# Short benchmark 总榜（spec-conformant-v2，推荐版）

## 结论摘要

这是当前唯一推荐使用的榜单。它以候选实际可见的 `TASKS.md` 为唯一 official contract，保留同一批 30 份模型产物（含 2 份 Cursor harness 跨平台产物）和原始 wire token，只修订 evaluator 的公开规范一致性。

- **A 条件严格榜第一**：`GPT/gpt-5.6-luna`（A07），4/4 tasks、16/16 official、2/2 extension、2/2 resource，306,032 tokens。
- **B 条件严格榜第一**：`mimo/mimo-v2.5`（B13），4/4、16/16、2/2、2/2，342,149 tokens。
- B 条件中 10 个模型达到 raw 16/16，其中 9 个 Gate 通过且进入严格榜完整分组；`mimo-v2.5-pro` 为 raw 15/16，但因 `.pytest_cache` 导致 Gate=0。
- 按 raw criteria 的 B−A：8/14 模型提升、5/14 不变、1/14 下降；平均 +1.07，median +1。
- 该结果支持“phi_3 计划通常提高代码完成度”，但不是无条件增益：`minimax-m3` 从 14/16 降至 12/16；多个已达 16/16 的模型只增加 token，没有 correctness 增益。
- 若目标是“强模型制定计划后选择弱模型执行”，本轮首选 **B13 `mimo-v2.5`**；若更看重无计划基线与低 token，A07 GPT、A04 Kimi、A14 GLM 都有不同优势。

## 评分口径

严格榜按 `manifest.json` 的词典序轴排序：

1. `InstructionGate`；
2. `StrictTaskCount`；
3. `OfficialCriterionCount`；
4. `ExtensionCapabilityCount`；
5. `ResourceCapabilityCount`；
6. token efficiency。

Gate 失败会把 strict tasks/official 清零，但表中始终保留 `Raw`，防止把指令违规误读为“没有实现”。宽松榜依次看 `ExecutionCompleted`、`RawCriterionCount`、acceptance、Gate compliance、extension 和 token efficiency，不做 Gate 清零。

## 严格榜 · A 条件（只读 `TASKS.md`）

| 排名 | Slot | 模型 | Gate | Tasks | Official | Raw | Ext | Res | Tokens | 失败 criterion |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | A07 | GPT/gpt-5.6-luna | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 306,032 | — |
| 2 | A14 | volcano/glm-5.2 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 426,426 | — |
| 3 | A06 | qwen/qwen3.8-max-preview | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 561,153 | — |
| 4 | A04 | kimi-code/kimi-for-coding | 1 | 4/4 | 16/16 | 16/16 | 1/2 | 2/2 | 194,101 | — |
| 5 | A03 | deepseek/deepseek-v4-pro | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 340,599 | `ttl_strict_types` |
| 6 | A08 | volcano/doubao-seed-2.1-turbo | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 729,724 | `rp_plain_dict` |
| 7 | A01 | MT/LongCat-2.0 | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 1/2 | 1,050,748 | `rp_plain_dict` |
| 8 | A09 | volcano/doubao-seed-2.0-pro | 1 | 3/4 | 15/16 | 15/16 | 1/2 | 2/2 | 223,366 | `rp_isolation` |
| 9 | A11 | volcano/minimax-m3 | 1 | 3/4 | 14/16 | 14/16 | 2/2 | 1/2 | 1,253,213 | `rp_plain_dict`, `rp_isolation` |
| 10 | A12 | mimo/mimo-v2.5-pro | 1 | 2/4 | 14/16 | 14/16 | 2/2 | 2/2 | 419,022 | `rp_plain_dict`, `ttl_gc_release` |
| 11 | A15 | composer/composer-2.5 † | 1 | 2/4 | 14/16 | 14/16 | 1/2 | 1/2 | N/A | `rp_plain_dict`, `ttl_strict_types` |
| 12 | A02 | deepseek/deepseek-v4-flash | 1 | 2/4 | 13/16 | 13/16 | 2/2 | 1/2 | 254,003 | `dl_deep_iterative`, `ttl_strict_types`, `ttl_gc_release` |
| 13 | A13 | mimo/mimo-v2.5 | 1 | 2/4 | 13/16 | 13/16 | 0/2 | 2/2 | 184,589 | `rp_isolation`, `du_units_ranges`, `du_normalize` |
| 14 | A05 | stepfun/step-3.7-flash | 1 | 1/4 | 12/16 | 12/16 | 2/2 | 1/2 | 591,861 | `rp_plain_dict`, `ttl_strict_types`, `ttl_gc_release`, `du_structured_errors` |
| 15 | A10 | volcano/doubao-seed-2.0-code | 1 | 1/4 | 12/16 | 12/16 | 1/2 | 1/2 | 379,863 | `rp_isolation`, `dl_deep_iterative`, `ttl_strict_types`, `ttl_gc_release` |

## 严格榜 · B 条件（额外读取 phi_3 计划）

| 排名 | Slot | 模型 | Gate | Tasks | Official | Raw | Ext | Res | Tokens | 失败 criterion / Gate 原因 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | B13 | mimo/mimo-v2.5 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 342,149 | — |
| 2 | B08 | volcano/doubao-seed-2.1-turbo | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 602,565 | — |
| 3 | B14 | volcano/glm-5.2 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 624,991 | — |
| 4 | B04 | kimi-code/kimi-for-coding | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 803,531 | — |
| 5 | B06 | qwen/qwen3.8-max-preview | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 863,422 | — |
| 6 | B01 | MT/LongCat-2.0 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 869,279 | — |
| 7 | B07 | GPT/gpt-5.6-luna | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 880,477 | — |
| 8 | B02 | deepseek/deepseek-v4-flash | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 900,470 | — |
| 9 | B05 | stepfun/step-3.7-flash | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | 326,756 | — |
| 10 | B03 | deepseek/deepseek-v4-pro | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | 1,407,484 | — |
| 11 | B15 | composer/composer-2.5 † | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | N/A | — |
| 12 | B09 | volcano/doubao-seed-2.0-pro | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 2/2 | 276,081 | `ttl_strict_types` |
| 13 | B10 | volcano/doubao-seed-2.0-code | 1 | 3/4 | 15/16 | 15/16 | 2/2 | 1/2 | 469,287 | `dl_deep_iterative` |
| 14 | B11 | volcano/minimax-m3 | 1 | 3/4 | 12/16 | 12/16 | 2/2 | 1/2 | 647,000 | 全部 4 个 dependency criteria |
| 15 | B12 | mimo/mimo-v2.5-pro | 0 | 0/4 | 0/16 | **15/16** | 2/2 | 2/2 | 190,320 | raw 仅失败 `ttl_strict_types`；Gate: `.pytest_cache` |

## 宽松榜 · A 条件

| 排名 | Slot | 模型 | Execution | Raw | Gate | Ext | Tokens |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | A07 | GPT/gpt-5.6-luna | 1 | 16/16 | 1 | 2/2 | 306,032 |
| 2 | A14 | volcano/glm-5.2 | 1 | 16/16 | 1 | 2/2 | 426,426 |
| 3 | A06 | qwen/qwen3.8-max-preview | 1 | 16/16 | 1 | 2/2 | 561,153 |
| 4 | A04 | kimi-code/kimi-for-coding | 1 | 16/16 | 1 | 1/2 | 194,101 |
| 5 | A03 | deepseek/deepseek-v4-pro | 1 | 15/16 | 1 | 2/2 | 340,599 |
| 6 | A08 | volcano/doubao-seed-2.1-turbo | 1 | 15/16 | 1 | 2/2 | 729,724 |
| 7 | A01 | MT/LongCat-2.0 | 1 | 15/16 | 1 | 2/2 | 1,050,748 |
| 8 | A09 | volcano/doubao-seed-2.0-pro | 1 | 15/16 | 1 | 1/2 | 223,366 |
| 9 | A12 | mimo/mimo-v2.5-pro | 1 | 14/16 | 1 | 2/2 | 419,022 |
| 10 | A11 | volcano/minimax-m3 | 1 | 14/16 | 1 | 2/2 | 1,253,213 |
| 11 | A15 | composer/composer-2.5 † | 1 | 14/16 | 1 | 1/2 | N/A |
| 12 | A13 | mimo/mimo-v2.5 | 1 | 13/16 | 1 | 0/2 | 184,589 |
| 13 | A05 | stepfun/step-3.7-flash | 1 | 12/16 | 1 | 2/2 | 591,861 |
| 14 | A02 | deepseek/deepseek-v4-flash | 0 | 13/16 | 1 | 2/2 | 254,003 |
| 15 | A10 | volcano/doubao-seed-2.0-code | 0 | 12/16 | 1 | 1/2 | 379,863 |

## 宽松榜 · B 条件

| 排名 | Slot | 模型 | Execution | Raw | Gate | Ext | Tokens |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | B05 | stepfun/step-3.7-flash | 1 | 16/16 | 1 | 2/2 | 326,756 |
| 2 | B13 | mimo/mimo-v2.5 | 1 | 16/16 | 1 | 2/2 | 342,149 |
| 3 | B08 | volcano/doubao-seed-2.1-turbo | 1 | 16/16 | 1 | 2/2 | 602,565 |
| 4 | B14 | volcano/glm-5.2 | 1 | 16/16 | 1 | 2/2 | 624,991 |
| 5 | B04 | kimi-code/kimi-for-coding | 1 | 16/16 | 1 | 2/2 | 803,531 |
| 6 | B06 | qwen/qwen3.8-max-preview | 1 | 16/16 | 1 | 2/2 | 863,422 |
| 7 | B01 | MT/LongCat-2.0 | 1 | 16/16 | 1 | 2/2 | 869,279 |
| 8 | B07 | GPT/gpt-5.6-luna | 1 | 16/16 | 1 | 2/2 | 880,477 |
| 9 | B02 | deepseek/deepseek-v4-flash | 1 | 16/16 | 1 | 2/2 | 900,470 |
| 10 | B03 | deepseek/deepseek-v4-pro | 1 | 16/16 | 1 | 2/2 | 1,407,484 |
| 11 | B15 | composer/composer-2.5 † | 1 | 16/16 | 1 | 2/2 | N/A |
| 12 | B09 | volcano/doubao-seed-2.0-pro | 1 | 15/16 | 1 | 2/2 | 276,081 |
| 13 | B12 | mimo/mimo-v2.5-pro | 1 | 15/16 | 0 | 2/2 | 190,320 |
| 14 | B11 | volcano/minimax-m3 | 1 | 12/16 | 1 | 2/2 | 647,000 |
| 15 | B10 | volcano/doubao-seed-2.0-code | 0 | 15/16 | 1 | 2/2 | 469,287 |

宽松榜将 `ExecutionCompleted` 放在 raw 之前，因此 B10 虽有 15/16，仍排在执行完整的 B11 之后；B12 不做 Gate 清零，所以能显示其真实 15/16。

## 14 模型 A/B delta

`Raw Δ`、`Task Δ` 和 `Token Δ` 均为 B−A。B12 的 `Task Δ=-2` 是 Gate 清零造成，不代表代码任务倒退；代码完成度应看 `Raw Δ=+1`。

| 模型 | A → B | Raw Δ | Strict task Δ | Gate Δ | Token Δ |
|---|---|---:|---:|---:|---:|
| GPT/gpt-5.6-luna | A07 → B07 | 0 | 0 | 0 | +574,445 |
| MT/LongCat-2.0 | A01 → B01 | +1 | +1 | 0 | -181,469 |
| deepseek/deepseek-v4-flash | A02 → B02 | +3 | +2 | 0 | +646,467 |
| deepseek/deepseek-v4-pro | A03 → B03 | +1 | +1 | 0 | +1,066,885 |
| kimi-code/kimi-for-coding | A04 → B04 | 0 | 0 | 0 | +609,430 |
| mimo/mimo-v2.5 | A13 → B13 | +3 | +2 | 0 | +157,560 |
| mimo/mimo-v2.5-pro | A12 → B12 | +1 | -2 | -1 | -228,702 |
| qwen/qwen3.8-max-preview | A06 → B06 | 0 | 0 | 0 | +302,269 |
| stepfun/step-3.7-flash | A05 → B05 | +4 | +3 | 0 | -265,105 |
| volcano/doubao-seed-2.0-code | A10 → B10 | +3 | +2 | 0 | +89,424 |
| volcano/doubao-seed-2.0-pro | A09 → B09 | 0 | 0 | 0 | +52,715 |
| volcano/doubao-seed-2.1-turbo | A08 → B08 | +1 | +1 | 0 | -127,159 |
| volcano/glm-5.2 | A14 → B14 | 0 | 0 | 0 | +198,565 |
| volcano/minimax-m3 | A11 → B11 | -2 | 0 | 0 | -606,213 |
| composer/composer-2.5 † | A15 -> B15 | +2 | +2 | 0 | N/A |

## † 跨 harness 标注

A15/B15（composer/composer-2.5）使用 Cursor harness 执行，token 数据不可用（N/A）。criterion、extension、resource 和 audit 评价与 kimi-code harness 模型完全公平可比。

## evaluator 修订清单

完整逐 criterion 证据见 `spec-conformance-audit-v2.md`。本版一次性做了以下规范修订：

1. `rp_plain_dict`：仍要求拒绝顶层 `dict` 子类，但不再绑定未公开的精确 `TypeError`。
2. `ttl_strict_types`：不可调用 clock 接受 `TypeError/ValueError`；通过构造后切换 clock 返回值，移除“构造器不得读取 clock”的未公开时机绑定。
3. `du_structured_errors`：保留精确 code；position 必须为稳定的非 bool int，并落在错误 token/字段跨度内；`1s2m` 的 order 接受 2 或 3。
4. 补回公开但旧 evaluator 漏测的约束：`DependencyCycleError(ValueError)`、`DurationParseError(ValueError)`、`parse_duration` 返回 plain `dict`。
5. 定向 mutant 已更新，新增 4 个 spec-v2 回归测试；reference 仍为 16/16，16/16 mutants 被捕获，Gate tamper 5/5。

## 哪些旧结论失效

- `final-leaderboard.md`、`final-leaderboard-contract-corrected.md`、`final-leaderboard-contract-corrected-v2.md` 仅供审计，不能再作为公平总榜。
- 旧榜中由 `du_structured_errors` 精确 position 2/3 引起的 A/B 差异全部失效。
- “B 计划让前若干模型达到 16/16”的旧解释曾混入 evaluator 对 `frozen-phi3-plan.md:113` 的语义对齐，不能直接等同于规划收益。
- 本版模型代码和 token 数据没有变化；变化仅是 evaluator 从 reference/plan-aligned 修正为 public-spec-aligned。

## Planner 与 token

- phi_3 planner：155,201 tokens（input 42,788；cache 95,232；output 17,181），按实验约定不计入候选 pipeline。
- 候选既有 wire 总量：A=6,914,700；B=9,203,812；合计 16,118,512 tokens。
- 本次 spec-v2 工作只重放本地 evaluator，没有重新调用候选模型，因此没有新增上述候选 inference token。

## B12 / mimo-v2.5-pro 明确解释

B12 并非“什么都没实现”：

- 四个模块均存在，公开 smoke 4/4；
- raw 15/16，唯一 correctness 失败为 `ttl_strict_types`：错误接受 `capacity=1.5`；
- extension 2/2、resource 2/2；
- 使用 190,320 tokens；
- 运行 `python -B -m pytest public_smoke_tests.py -v` 后产生 `.pytest_cache`。`-B` 只禁止 `.pyc`，不禁止 pytest cache，因此 Gate 原因是 `unexpected workspace entry .pytest_cache`；
- strict 仍必须是 0/4、0/16，lenient/raw 才体现代码真实完成度。禁止 posthoc 删除 cache 后冒充原始单次结果。

## 验证与产物

- 资产冻结：48 assets verified，动态 `runs/`、`results/` 排除；
- harness：13/13 tests；
- reference：4/4 strict tasks、16/16 official；
- mutants：16/16 caught；
- Gate tamper：5/5；
- 正式重评：30 entries，A=15、B=15。

机器可读结果：

- `formal-spec-conformant-v2/A01.json` … `B14.json`
- `final-report-spec-conformant-v2.json`
- `spec-conformance-audit-v2.md`

历史结果目录和三份旧报告均保留，未覆盖。
