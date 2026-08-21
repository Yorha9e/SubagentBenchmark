# Critic Pilot — debug-subagent-v1-critic-v1

单轮只读 Critic 缺陷发现测试（pilot，3 个现有候选产物，不重跑、不修改候选）。

## 协议

- 每候选恰好一次 `critic` 子代理调用（同一 profile，实际模型 `GPT/gpt-5.6-sol`），单轮、无追问。
- 输入盲化：候选复制为 `inputs/candidate-A|B|C/`，仅含公开 `TASKS.md`、`solutions/dependency_layers.py`、`public_smoke_tests.py`。
- Critic 禁止运行代码、联网、读取隐藏 evaluator / bug 报告 / 其他候选。
- 计时：`parent_wall_clock_serial` — 父控在派发前、返回后各取一次 epoch 时间，三候选严格串行。含模型排队与生成时间及约 0.1–1s 工具调度开销；非 monotonic。candidate-A 含首次派发 warmup。
- findings 由主控在 Critic 完成后做经验复现，并对照隐藏 evaluator（`reviewer-b11-external-v2`）replay-v2 结果确认；Critic 本身未接触这些。
- token 用量：Agent 工具结果不暴露 usage，记为 unavailable。

## 候选映射

| Blind ID | 真实候选 | 模型 |
|---|---|---|
| candidate-A | round-2/subtest_12 | mimo/mimo-v2.5-pro |
| candidate-B | round-1/subtest_7 | GPT/gpt-5.6-luna |
| candidate-C | round-2/phi_2 | volcano/glm-5.2 |

## 结果

| 候选 | 总发现耗时 (s) | findings | 确认 | 误报 | 最大深度 | 命中隐藏 GT | 漏报隐藏 GT |
|---|---|---|---|---|---|---|---|
| candidate-A (subtest_12) | 251.205 | 2 | 2 | 0 | L4 | cross_hashability | — |
| candidate-B (subtest_7) | 70.062 | 1 | 1 | 0 | L4 | (无隐藏失败项) | — |
| candidate-C (phi_2) | 163.481 | 2 | 2 | 0 | L3 | cross_hashability | — |

隐藏 ground truth（replay-v2，dependency_layers 相关）：subtest_12 与 phi_2 唯一失败项均为补充检查 `cross_hashability`；subtest_7 全过。Critic 在两个有缺陷候选上都命中该项，零漏报、零误报。

## 主要 findings

- A-F1 / C-F2（confirmed，跨可哈希域去重缺失）：hashable 与 unhashable 相等值分属两个注册表，互不比较 → 同一逻辑节点拿到两个 id。复现：`dependency_layers([(1,0),(U(),0)])` 得 3 节点 `[[0],[1,U]]`，应为 2 节点。与隐藏检查 `cross_hashability` 失败一致。subtest_7 的实现有跨域交叉查找，故无此缺陷。
- A-F2 / B-F1 / C-F1（confirmed，unhashable 注册表 O(N²)）：线性扫描导致二次方增长。实测 2× 输入 → 3.9–4.2× 耗时；B 因双向跨域扫描绝对耗时约为 A/C 的 4.3 倍（N=3000: 0.837s vs ~0.19s）。隐藏 evaluator 的 50k 规模检查只用 hashable 节点，未覆盖此点 — Critic 发现了评测体系外的真实资源缺陷。

## 观察（对"为 mimo-v2.5-pro 类 subagent 配 critic"的含义）

- 单轮 Critic 已足以在无隐藏答案条件下命中全部已知正确性缺陷，且给出可执行验证输入 → 适合做快速反馈环的第一环。
- 深度分布：A/B 达 L4（系统性资源），C 达 L3；三者均超过"表面症状"层。
- 耗时差异（70s vs 251s）主要来自模型生成长度与首次派发 warmup，样本量 3 不足以下结论；正式轮需固定派发顺序轮换或多次重复。

## 文件

- `candidate-map.json` — 映射、协议、审查前后全树 SHA-256（审查后逐字节未变，`post_review_unchanged: true`）
- `inputs/candidate-{A,B,C}/` — 盲化输入副本（含各文件 SHA-256）
- `reviews/candidate-{A,B,C}.raw.json` — Critic 原始输出
- `reviews/candidate-{A,B,C}.json` — 含计时、确认状态、GT 对齐的结构化结果
- `timing-summary.json` / `finding-summary.json`

本结果独立于 `debug-subagent-v1-replay-v2` 确定性排名，不并入排行榜。
