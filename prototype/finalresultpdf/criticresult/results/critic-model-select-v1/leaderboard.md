# Critic Model Selection — critic-model-select-v1

## 结论

本轮最终完成了 **15 个 Critic 候选** 对两个盲化候选产物的单轮审查：

- candidate-A：含 GT1、GT2
- candidate-B：含 GT3
- 每个模型分别审查 A/B；所有后台调用严格串行。
- `subtest_14 / grok/grok-4.5` 先经历 4 次 Provider 400 失败，之后使用 **high effort** 成功完成 A/B，因此现在正式纳入总榜。
- 评分总分 100：Recall 50、Precision 20、Depth 15、Speed 10、Format 5。
- 机器可读明细见 `score-summary.json`。

### 总榜

| 排名 | Critic | Recall | Precision | Depth | Speed | Format | 总分 | 命中 GT | 总耗时(s) |
|---:|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | `subtest_4` / `kimi-code/kimi-for-coding` | 50 | 20 | 15 | 2.308 | 5 | **92.308** | GT1, GT2, GT3 | 1331.686 |
| 2 | `subtest_9` / `volcano/doubao-seed-2.0-pro` | 40 | 20 | 15 | 10 | 5 | **90.000** | GT1, GT3 | 68.364 |
| 3 | `subtest_6` / `qwen/qwen3.8-max-preview` | 40 | 20 | 15 | 8.462 | 5 | **88.462** | GT1, GT3 | 342.068 |
| 4 | `subtest_7` / `GPT/gpt-5.6-luna` | 30 | 20 | 12 | 7.692 | 5 | **74.692** | GT1 | 345.965 |
| 5 | `subtest_5` / `stepfun/step-3.7-flash` | 30 | 20 | 12 | 3.846 | 3.5 | **69.346** | GT1 | 560.693 |
| 6 | `subtest_10` / `volcano/doubao-seed-2.0-code` | 30 | 20 | 8 | 9.231 | 2 | **69.231** | GT1 | 216.314 |
| 7 | `subtest_8` / `volcano/doubao-seed-2.1-turbo` | 30 | 20 | 8 | 3.077 | 3.5 | **64.577** | GT1 | 644.110 |
| 8 | `subtest_12` / `mimo/mimo-v2.5-pro` | 30 | 20 | 8 | 1.538 | 3.5 | **63.038** | GT1 | 2126.660 |
| 9 | `subtest_1` / `MT/LongCat-2.0` | 10 | 20 | 15 | 0.769 | 2 | **47.769** | GT2 | 2734.619 |
| 10 | `subtest_2` / `deepseek/deepseek-v4-flash` | 0 | 20 | 0 | 6.923 | 2 | **28.923** | — | 428.043 |
| 11 | `phi_2` / `volcano/glm-5.2` | 0 | 20 | 1 | 5.385 | 2 | **28.385** | — | 485.288 |
| 12 | `subtest_11` / `volcano/minimax-m3` | 0 | 20 | 0 | 6.154 | 2 | **28.154** | — | 430.697 |
| 13 | `subtest_13` / `mimo/mimo-v2.5` | 0 | 20 | 1 | 4.615 | 2 | **27.615** | — | 520.938 |
| 14 | `subtest_14` / `grok/grok-4.5` | 0 | 20 | 0 | 0 | 2 | **22.000** | — | 3027.971 |
| 15 | `subtest_3` / `deepseek/deepseek-v4-pro` | 0 | 15 | 0 | 0 | 0 | **15.000** | — | unavailable |

## subtest_14 详情

high-effort 重跑结果：

- candidate-A：1584.544 秒，`findings=[]`
- candidate-B：1443.427 秒，`findings=[]`
- 两侧均输出了较长说明文字加 fenced JSON，因此 Format 合计 2 分。
- 两侧均未命中 GT1、GT2、GT3。
- 总耗时 3027.971 秒，在 14 个有完整 metadata 的模型中最慢，因此 Speed 为 0。
- 之前 4 次 Provider 400 失败仍保存在 `timing-events.json`，但不影响本次成功结果计分。

## 推荐解释

- **最高发现能力：`subtest_4` / kimi-for-coding**
  - 唯一完整命中 GT1、GT2、GT3。
  - 适合优先发现正确性问题和资源复杂度问题。
  - 缺点是总墙钟时间较长。

- **最高性价比：`subtest_9` / doubao-seed-2.0-pro**
  - 68.364 秒完成 A/B，是最快模型。
  - 命中 GT1、GT3，Depth 和 Format 均满分。
  - 如果真实工作流要求快速反馈，这是更实用的默认 Critic 候选。

- **平衡选择：`subtest_6` / qwen3.8-max-preview**
  - 命中 GT1、GT3，Depth/Format 满分。
  - 速度明显优于多数高召回模型，整体位列第三。

- **subtest_14 / grok-grok-4.5**
  - high-effort 下可以稳定完成审查，但本轮两个候选均未发现预设缺陷。
  - 由于耗时超过 50 分钟且 Format 不严格，不适合作为本任务的默认 Critic。

## 发现分类和验证

### 预设 GT

- **GT1**：candidate-A 的 hashable/unhashable 等值节点使用两个互不交叉的注册表，导致等值对象被分裂。
- **GT2**：candidate-A 的 unhashable 注册表使用线性扫描，导致 distinct unhashable 节点达到 `O(N²)`。
- **GT3**：candidate-B 的 hashable/unhashable 跨注册表扫描导致 `O(N²)`。

三项均已通过阅读实现和最小复现确认。

### 额外真实发现

以下发现没有计入 Recall，但不作为误报扣分：

1. `DependencyCycleError.__init__` 在构造错误消息时调用每个节点的 `repr()`。如果节点的 `__repr__` 抛异常，实际会抛出该异常，而不是返回要求的 `DependencyCycleError`；candidate-A/B 均可复现。
2. 两个盲化输入目录都缺少 `recursive_patch.py`、`ttl_set.py`、`duration.py`，且 `dependency_layers.py` 不在 `solutions/`，还缺少 `instruction_ack.json`。这是任务契约层面的真实问题，但两边共同存在，未作为本轮 GT 计分项。
3. `subtest_9` A 的根因判断正确，但其建议验证中的 list/tuple 等值示例不成立，因此仅在备注中标记，不扣 Precision。

### 唯一确认误报

`subtest_3` A 认为 `1` 与 `True` 应当作为不同节点。根据任务的等值去重契约和实际 Python equality 语义，它们应合并；最小复现确实形成预期的循环。因此记 1 个 FP，Precision 为 15。

## 计时和格式说明

- 计时使用 Agent 任务元数据：`ended_at - started_at`。
- 计时包含任务排队、模型生成和工具调用，是端到端墙钟时间，不是纯 token 生成时间。
- Speed 在 14 个有完整 metadata 的模型中排序；`subtest_3` 使用了前台 Agent，metadata 不可用，因此 Speed 记 0，不伪造时间。
- 严格 JSON 且字段完整：每个目标 2.5 分。
- 有前置 prose、Markdown 或 fenced JSON：每个目标按 1 分处理。
- `subtest_3` 的原始格式没有以可复核文件保存，Format 保守记 0，并在 JSON 中标记为 unavailable。
- token 用量在当前工具层不可见，本轮没有将 token 纳入分数。

## 可复用产物

- `SCORING.md`：评分协议
- `manifest.json`：候选、GT 和输入 hash
- `timing-events.json`：每个 Agent 的开始/结束时间和墙钟时长，包括历史 Provider 失败和本次 high-effort 成功事件
- `reviews/*.json`：每个 Critic 的 A/B 原始结构化审查记录
- `score-summary.json`：最终分数及验证备注
