# Short-task benchmark archive

本目录是短任务 benchmark 的只读归档副本，汇总原始 15 个模型与后续两个 supplemental 模型的运行产物和评测结果。

## 归档范围

- 模型总数：17
- A 条件 cells：17（A01–A17）
- B 条件 cells：17（B01–B17）
- 总 evaluation entries：34

模型来源：

- A01–A15 / B01–B15：原始 `short` benchmark 正式模型。
- A16 / B16：`subtest_14`，模型 `grok/grok-4.5`，high effort，隔离 supplemental run。
- A17 / B17：`subtest_15`，模型 `tx/hy3`，max effort，使用全英文 subagent prompt 的隔离 supplemental run。

## A/B 条件

- A：候选只读取公开 `TASKS.md` 和 public smoke materials。
- B：候选额外读取冻结的 `phi_3` 实施计划。

## 目录

- `formal-15-models/benchmark/`：正式 benchmark 的 manifest、任务说明、设计文档、冻结资产 hash 和共享计划。
- `formal-15-models/workspaces/prepared/`：30 个正式候选 workspace，包括 solution、cell metadata、instruction ack、usage/events（若存在）及运行遗留证据。
- `formal-15-models/evaluations/formal-spec-conformant-v2/`：30 个正式评测 JSON。
- `formal-15-models/reports/`：推荐正式榜、总表、机器报告、维度报告和 evaluator 契约审计。
- `supplemental/subtest14-grok-high/`：A16/B16 workspace、evaluation 和报告。
- `supplemental/subtest15-english/`：A17/B17 workspace、evaluation 和报告。
- `combined-leaderboard/`：含两个 supplemental 模型的 17 模型扩展总榜及机器报告。
- `archive-manifest.json`：归档文件的 SHA-256、大小、来源根目录和汇总计数。

## 冻结与证据说明

本目录通过复制生成；没有移动、修改或重新评测来源数据。原始冻结内容仍位于：

- `short/`
- `short_subtest14_grok_high/`
- `short_subtest15_english/`

A17/B17 等 supplemental 结果不改写原正式 15 模型冻结榜。B17 workspace 中的 `.pytest_cache` 是 Instruction Gate 失败的原始证据，必须保留；本归档不会 posthoc 清理它。`__pycache__`、`cell.json`、`instruction_ack.json`、public inputs、solution files 和 usage/events 也按来源原样归档。

## 完整性校验

`archive-manifest.json` 不包含自身 hash，其 `files` 数组覆盖目录内其余归档文件。可逐项重算 SHA-256，并与 `sha256` 字段比较。
