# Critic 隔离测试：doubao-seed-evolving

## 测试信息

- Run ID：`critic-doubao-evolving-v1`
- 模型：`volcanoagent/doubao-seed-evolving`（slot `subtest1`，thinking_effort `high`）
- 协议：`critic-model-select-v1`
- 测试日期：2026-07-27
- 隔离目录：`criticresult/results/critic-doubao-evolving-v1/`
- 计时来源：Agent task metadata wall clock（后台任务）

## 评分

| 维度 | 得分 | 满分 | 说明 |
|---|---:|---:|---|
| Recall | **50** | 50 | GT1 ✓ (30) + GT2 ✓ (10) + GT3 ✓ (10) |
| Precision | **20** | 20 | 0 误报 |
| Depth | **15** | 15 | A 侧 depth_level = 4（最高） |
| Speed | **2.308** | 10 | 总耗时 1354.3s，14 模型中排第 11 |
| Format | **5** | 5 | 两目标均严格 JSON、字段完整 |
| **总分** | **92.308** | 100 | |

## 计时

| 候选 | agent_id | 耗时 |
|---|---|---:|
| candidate-A | agent-238 | 590.4s |
| candidate-B | agent-239 | 763.8s |
| **合计** | | **1354.3s** |

## GT 命中详情

| GT | 目标 | 类型 | 分值 | 命中 | 对应 finding |
|---|---|---|---:|---|---|
| GT1 跨哈希域相等值去重缺失 | A | 正确性 | 30 | ✓ | A-F1 |
| GT2 unhashable 注册表 O(N²) | A | 资源 | 10 | ✓ | A-F2 |
| GT3 双向跨域扫描 O(N²) | B | 资源 | 10 | ✓ | B-F1 |

doubao-seed-evolving 是继 `kimi-for-coding` 之后**第二个命中全部三个 GT** 的模型。

B-F2 是一个额外的真实性能发现（hashable lookup 上的无条件 O(U) 扫描），不对应 GT，但也不是误报。

## 与现有 critic 榜对比（排除 gpt/cc 系，N=14）

| 排名 | 模型 | Recall | Precision | Depth | Speed | Format | 总分 | GT 命中 | 总耗时 |
|---:|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | `kimi-for-coding` | 50 | 20 | 15 | 3.077 | 5 | **93.077** | GT1,GT2,GT3 | 1331.7s |
| 2 | `doubao-seed-evolving` | 50 | 20 | 15 | 2.308 | 5 | **92.308** | GT1,GT2,GT3 | 1354.3s |
| 3 | `doubao-seed-2.0-pro` | 40 | 20 | 15 | 10 | 5 | **90.000** | GT1,GT3 | 68.4s |
| 4 | `qwen3.8` | 40 | 20 | 15 | 8.462 | 5 | **88.462** | GT1,GT3 | 342.1s |

注：排除 gpt 后 N=14，kimi-for-coding 的 speed 重算为 3.077（原 N=15 时为 2.308）。

## 关键结论

doubao-seed-evolving 全中三个 GT，recall 与 kimi-for-coding 持平，但总耗时 1354.3s 比 kimi-for-coding 的 1331.7s 略慢 23 秒。两者在 critic 维度上几乎完全持平，差距仅 0.77 分（speed 排名差 1 位）。

速度-召回 tradeoff 依然存在：全中 GT 的两个模型都做了大量实测验证，都慢（~1330-1355s）；快出结论的 doubao-seed-2.0-pro（68s）靠直接推理，代价是漏 GT2。

doubao-seed-2.0-pro 复测正在进行中（agent-240, subtest2 slot），用于验证其原始 68s 计时是否可复现。

## 文件清单

```
reviews/candidate-A.json             # 首次 A 审查（前台，无计时）
reviews/candidate-B.json             # 首次 B 审查（前台，无计时）
reviews/candidate-A-rerun2.json      # 后台 A 审查（有计时）
reviews/candidate-B-rerun2.json      # 后台 B 审查（有计时）
reviews/doubao-seed-evolving.json    # 结构化合并审查
score-summary.json                   # 评分明细（含计时）
timing-events.json                   # 计时元数据
leaderboard.md                       # 本文件
```
