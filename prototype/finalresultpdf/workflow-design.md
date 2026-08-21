# SubagentBenchmark 工作流设计文档

版本：v2.0 · 2026-07-30

## 1. 概述

基于 SubagentBenchmark 四轴测试（短任务 24 候选 · 长任务 27 候选 · Reviewer 20 参评 · Critic 21 候选）的全部数据，设计一套以 Main agent 为调度核心、多模型 subagent 协作的工作流体系。

排除 gpt/cc 系模型（账号不可用）。排除 deepseek 系模型（额度耗尽）。

## 2. 自定义 Profile

五个自定义 subagent profile，安装在 `~/.omkc/agents/`：

### 2.1 short-coder

| 属性 | 值 |
|---|---|
| 用途 | 短任务实现（单模块、函数级、benchmark 风格） |
| 工具 | Read, Write, Edit, Bash, Grep, Glob, TodoList |
| 核心行为 | 契约精度优先；强制检查类型安全、排序、复杂度、跨类型等值 |
| 不允许 | 修改 TASKS.md / smoke tests / 读取 evaluator |

### 2.2 long-coder

| 属性 | 值 |
|---|---|
| 用途 | 长任务实现（多模块后端系统、闭环项目） |
| 工具 | Read, Write, Edit, Bash, Grep, Glob, TodoList, Skill |
| 核心行为 | 系统级思维；强制测试持久化/reopen、并发安全、CLI 端到端 |
| 不允许 | 修改 TASKS.md / BRIEFING.md / src/__init__.py / 读取 evaluator |

### 2.3 code-critic

| 属性 | 值 |
|---|---|
| 用途 | 只读代码审查，发现 bug 并输出结构化 JSON |
| 工具 | Read, Grep, Glob, Bash, Write（**禁用 Edit**） |
| 核心行为 | 系统性验证；写临时测试脚本确认假设；零误报原则 |
| 不允许 | 修改源码文件（Edit 被工具层禁用）；在 workspace 中创建文件 |

### 2.4 code-reviewer

| 属性 | 值 |
|---|---|
| 用途 | Debug 和修复已有代码中的 bug |
| 工具 | Read, Write, Edit, Bash, Grep, Glob, TodoList, Skill |
| 核心行为 | 最小化修改；内置检查清单（类型/排序/复杂度/等值/资源/并发/持久化） |
| 不允许 | 修改 TASKS.md / smoke tests / 读取 evaluator |

### 2.5 code-scout

| 属性 | 值 |
|---|---|
| 用途 | 前期调研、代码库探索、依赖分析、需求汇总 |
| 工具 | Read, Grep, Glob, Bash, WebSearch, FetchURL（**禁用 Write/Edit**） |
| 核心行为 | 只读探索；输出结构化 research brief（Context/State/Requirements/Risks/Recommendations） |
| 不允许 | 修改任何文件；写实现计划（那是 Main 的职责） |

### 2.6 code-coder（通用兜底）

| 属性 | 值 |
|---|---|
| 用途 | 通用实现，无特定侧重 |
| 工具 | 全工具 |
| 核心行为 | 标准 coder 行为 + 基础约束 |

## 3. 模型分配

### 3.1 供应商-模型分配

7 个供应商，8 个模型，9 个角色。每个供应商最多 2 个模型，角色间串行不冲突。

| 供应商 | 选定模型 | slot | 角色 | 关键数据 |
|---|---|---|---|---|
| **volcano** | glm-5.2 | phi_2 | 短任务 Coder | 短 A 16/16 满分 · 426k · 530s |
| **volcano** | doubao-seed-2.0-pro | subtest2 | Scout（风险分析） | Critic 90 · 68s · 跨模块风险评估 |
| **Google** | gemini-3.6-flash-tiered | subtest3 | Critic + Reviewer | Critic GT全中·133s · Reviewer 8/8·60ms · 两轮一致 |
| **qwen** | qwen3.8-max-preview | subtest6 | 长任务 Coder | 长 8/10 断层第一 · 短 16/16 |
| **kimi-code** | kimi-for-coding | subtest4 | 交叉 Critic | Critic 92.3 GT全中 · Reviewer 8/8 |
| **mimo** | mimo-v2.5-pro | subtest12 | 省钱 Coder | 短 B 190k 最省 · 14/16 可修复 |
| **MT** | LongCat-2.0 | longcat | 性能 Critic + 信息 Scout | 缓存命中近免费 · GT2 独特 · 15/16 理解力 |
| **stepfun** | step-3.7-flash | subtest5 | 计划执行器 | 有计划 16/16 · 327k 最省 |

v2.0 变更：evolving 被 gemini-3.6-flash 替换（同分但快 10 倍）；deepseek 系移除（额度耗尽）；doubao-2.1-turbo 移除（3.6-flash 兼任快速 reviewer）；信息 scout 从 deepseek-flash 改为 LongCat（理解力更强且免费）。

### 3.2 并行能力

```
短任务：glm-5.2 写代码 (volcano) ──> 3.6-flash 审查 (Google)     不同供应商，可并行
长任务：qwen 写代码 (qwen)       ──> 3.6-flash 审查 (Google)     不同供应商，可并行
交叉审：3.6-flash 审完 (Google)  ──> kimi 复审 (kimi-code)        串行 OK
信息scout：LongCat (MT) 在代码前   性能critic：LongCat (MT) 在代码后  首尾不冲突
```

### 3.3 角色与供应商对照

| 角色 | 模型 | 供应商 | profile | 说明 |
|---|---|---|---|---|
| Scout（信息汇总） | LongCat-2.0 | MT | `code-scout` | 免费 · 15/16 · 大上下文 |
| Scout（风险分析） | doubao-2.0-pro | volcano | `code-scout` | 68s · Critic 90 |
| 短任务 Coder（省心） | glm-5.2 | volcano | `short-coder` | 16/16 一次过 |
| 短任务 Coder（省钱） | mimo-v2.5-pro | mimo | `short-coder` | 190k + critic 修复 |
| 长任务 Coder | qwen3.8 | qwen | `long-coder` | 8/10 不可替代 |
| 计划执行器 | step-3.7-flash | stepfun | `short-coder` | 有 plan 时 16/16 |
| 深度 Critic | gemini-3.6-flash | Google | `code-critic` | GT全中 · 133s · 零误报 |
| 交叉 Critic | kimi-for-coding | kimi-code | `code-critic` | 第二意见 |
| 性能 Critic（免费） | LongCat-2.0 | MT | `code-critic` | 仅采纳性能类 finding |
| 深度+快速 Reviewer | gemini-3.6-flash | Google | `code-reviewer` | 8/8 · 60ms · 两轮一致 |

### 3.4 已排除模型

| 模型 | 供应商 | 排除原因 | 保留备注 |
|---|---|---|---|
| doubao-seed-evolving | volcano | 被 3.6-flash 替换 | Critic 92.3 · Reviewer 8/8，作为 backup 保留 |
| gemini-3.6-flash | deepseek | 额度耗尽 | Reviewer 8/8 · 60ms |
| LongCat-2.0 | deepseek | 额度耗尽 | 短 B 16/16 · 免费（缓存） |
| doubao-2.1-turbo | volcano | 3.6-flash 兼任快速 reviewer | Reviewer 7/8 · 115ms |
| grok-4.5 | grok | 额度较少 | 短 A 16/16，额度充足时可启用 |
| gemini-3-flash / 3.1-pro / 3.5-flash / pro-agent | Google | 3.6-flash 全面优于同门 | 长任务 0-9/20，critic 均漏 GT |
| hy3 | tx | 太贵且能力不突出 | 短 A 14/16，需英文 prompt |
| doubao-seed-2.0-code | volcano | 全轴垫底 | 无使用场景 |
| minimax-m3 | volcano | 计划反向 · 无突出能力 | Reviewer 7/8 · 121ms |
| mimo-v2.5 | mimo | 已选 v2.5-pro | 短 B 342k，v2.5-pro 的 190k 更省 |

## 4. 工作流模式

### 4.1 标准调研 + 短任务流（省心模式）

```
Main 读任务
  -> code-scout (doubao-2.0-pro) 前期调研     68s · 代码库探索 + 需求汇总
  -> short-coder (glm-5.2) 写实现             426k token · 530s
  -> code-critic (gemini-3.6-flash) 审查              133s · GT全中 · 两轮一致
  -> [如有问题] short-coder 修复
  -> 完成
```

特点：scout 先摸清现状（68s 快速），coder 再动手，critic 最后审查。三步串行，volcano 内不并发。适合不熟悉代码库的新任务。

### 4.1a Scout 场景矩阵

同一 `code-scout` profile，按场景切 binding_slot：

| 场景 | 模型 | slot | 成本 | 理解力 | 适合 |
|---|---|---|---|---|---|
| 查文件位置 + 读 API | mimo-v2.5-pro | subtest12 | 190k 最省 | 14/16 | 极简探索，mimo 先 scout 再 code |
| 信息汇总 + 现状梳理 | LongCat-2.0 | subtest2f | 免费（缓存） | 13/16 | 读取文件 + 汇总现状 |
| 跨模块风险 + 性能评估 | doubao-2.0-pro | subtest2 | 223k | 15/16 + Critic 90 | 风险识别 + 复杂度分析 |
| 大型代码库全局映射 | LongCat-2.0 | longcat | 免费（缓存） | 15/16 | 150M 上下文，一次性读整个代码库 |
| 长任务前置架构分析 | qwen3.8 | subtest6 | 561k | 16/16 + Critic 88.5 | qwen 先 scout 再 long-coder |

选择原则：
- **成本优先**：mimo-v2.5-pro（190k）或 LongCat（免费）
- **质量优先**：doubao-2.0-pro（Critic 90）或 qwen3.8（16/16 + 88.5）
- **大代码库**：LongCat（150M 上下文 + 缓存免费）
- **长任务前置**：qwen3.8（scout + implement 同模型，减少信息传递损耗）

### 4.2 省钱短任务流

```
Main 读任务
  → short-coder (mimo-v2.5-pro) 写实现     190k token · 最省
  → code-critic (gemini-3.6-flash) 审查            发现 2-3 个定点缺陷
  → short-coder (mimo-v2.5-pro) 按反馈修复  ~50k token
  → code-critic (gemini-3.6-flash) 复审
  → 完成
```

特点：mimo-v2.5-pro token 最省（190k vs glm-5.2 的 426k，省 55%），但需要 2 轮。总 coder token 约 240k，比省心模式还省 44%。critic 异步不阻塞。

### 4.3 标准长任务流

```
Main 读任务 + BRIEFING
  → long-coder (qwen3.8) 实现项目 A        长任务 #1 · 8/10 strict
  → long-coder (qwen3.8) 实现项目 B
  → code-critic (gemini-3.6-flash) 审查两项目
  → [如有问题] long-coder 修复
  → 完成
```

特点：qwen3.8 在长任务上断层第一（8/10，第二名 6/10），不可替代。critic 做最终质量门。

### 4.4 双 critic 交叉审查（高可靠性）

```
Main 读任务
  → coder 写实现
  → code-critic (gemini-3.6-flash) 深度审查         GT全中 · 1354s
  → code-critic (kimi) 交叉审查             GT全中 · 1332s
  → 合并两份 findings
  → coder 修复所有确认缺陷
  → 完成
```

特点：两个不同模型交叉审查，消除单一模型盲区。gemini-3.6-flash 和 kimi 总分相同但行为模式不同（3.6-flash 速度 10 倍优势，kimi 推理更细）。适合高可靠性需求。

### 4.5 两段式审查（快速 + 深度）

```
Main 读任务
  → coder 写实现
  → code-critic (doubao-2.0-pro) 快速预筛   68s · 90分 · 可能漏 GT2
  → [如发现明显问题] 立刻反馈 coder 修复
  → code-critic (gemini-3.6-flash) 深度审查         133s · GT全中 · 两轮一致 · 补 GT2
  → 完成
```

特点：68 秒快速反馈解决明显问题，1354 秒深度审查兜底深层缺陷。适合需要快速响应但又不能漏 bug 的场景。

### 4.6 计划驱动流（有详细 plan 时）

```
Main 分析任务 → 制定详细 plan
  → short-coder (step-3.7-flash) 照 plan 执行   327k token · 最省
  → code-critic (gemini-3.6-flash) 审查
  → [如有问题] 修复
  → 完成
```

特点：step-3.7-flash 无计划时只有 12/16，但有详细计划后 16/16 且 token 最省（327k）。Main 承担 planner 角色，flash 做"规格执行器"。

### 4.7 独立 Debug 流（按需）

```
Main 收到 bug 报告
  → code-reviewer (gemini-3.6-flash) 诊断 + 修复     8/8 · 79.8ms 性能最快
  → 完成
```

特点：gemini-3.6-flash 在 Reviewer 榜 #1（8/8 + 60ms 全榜最快），独立于日常 pipeline，按需调用。

### 4.8 快速 Debug 迭代流

```
Main 收到 bug 报告
  → code-reviewer (gemini-3.6-flash) 快速修复   8/8 · 60ms
  → [如修不了] code-reviewer (gemini-3.6-flash) 精修    8/8 · 79.8ms
  → 完成
```

特点：3.6-flash 同时负责深度和快速审查（8/8 · 60ms 兼任）。适合需要快速迭代的场景。

### 4.9 免费性能补充审查

```
Main 读任务
  -> coder 写实现
  -> code-critic (gemini-3.6-flash) 深度审查           1354s · GT1/2/3 全中 · 主审
  -> code-critic (LongCat) 性能补充审查         2735s · 缓存命中近免费 · 仅取性能类 finding
  -> 合并 findings（LongCat 只采纳性能/资源类，正确性类以 3.6-flash 为准）
  -> coder 修复
  -> 完成
```

特点：LongCat 缓存命中后近免费，异步后台跑不阻塞主流程。它在 Critic 盲审中唯一命中 GT2（O(N²) 性能缺陷）但未命中 GT1/GT3，说明对性能问题有特殊敏感度。作为 3.6-flash 之后的第二意见，专门覆盖性能维度。注意：LongCat 正确性类 finding 不可靠（GT1 未命中），只采纳其性能/资源类报告。

**LongCat 缓存说明**：短任务缓存命中率低（~1.6%，任务太短缓存未积累）；长任务/大上下文场景理论命中率可达 92%（138M/150M）。作为额外 critic 在后台异步运行，即使慢（2735s）也不阻塞主流程。

## 5. Main Agent 职责

Main agent（主 agent）承担以下职责，不派发给 subagent：

| 职责 | 说明 |
|---|---|
| **Planner** | 读任务、拆解、决定用哪个 profile 和模型 |
| **Orchestrator** | 串行/并行派发 subagent、控制流程 |
| **Prompt 组装** | 读取任务 spec、填入 workspace 路径和约束 |
| **结果收集** | 收 subagent 返回、跑 evaluator |
| **反馈路由** | 读 critic findings、转化为 coder 修复指令 |
| **质量门控** | 决定是否通过、是否需要再迭代 |

## 6. Slot 配置参考

`.kimi-code/local.toml` 中的 slot 绑定（由用户自行配置）：

```toml
# === 主力配置（7 供应商 8 模型） ===

# volcano - 短任务 Coder
[subagent-slot.phi_2]
model = "volcano/glm-5.2"
thinking_effort = "high"

# volcano - Scout（风险分析）
[subagent-slot.subtest2]
model = "volcanoagent/doubao-seed-2.0-pro"
thinking_effort = "high"

# Google - Critic + Reviewer
[subagent-slot.subtest3]
model = "google/gemini-3.6-flash-tiered"
thinking_effort = "high"

# qwen - 长任务 Coder
[subagent-slot.subtest6]
model = "qwen/qwen3.8-max-preview"
thinking_effort = "high"

# kimi-code - 交叉 Critic
[subagent-slot.subtest4]
model = "kimi-code/kimi-for-coding"
thinking_effort = "high"

# mimo - 省钱 Coder
[subagent-slot.subtest12]
model = "mimo/mimo-v2.5-pro"
thinking_effort = "high"

# MT - 性能 Critic + 信息 Scout
[subagent-slot.longcat]
model = "MT/LongCat-2.0"
thinking_effort = "high"

# stepfun - 计划执行器
[subagent-slot.subtest5]
model = "stepfun/step-3.7-flash"
thinking_effort = "high"

# === 按需启用（已排除，保留备注） ===
# [subagent-slot.subtest8]  # volcano/doubao-seed-2.1-turbo - 快速 reviewer 115ms
# [subagent-slot.subtest14] # grok/grok-4.5 - 短 A 满分，额度充足时启用
```

## 7. 测试数据支撑

### 7.1 短任务 A 条件满分模型（排除 gpt）

| 模型 | Official | Ext | Res | Token | 耗时 |
|---|---:|---:|---:|---:|---:|
| doubao-seed-evolving | 16/16 | 2/2 | 2/2 | N/A | 466s |
| glm-5.2 | 16/16 | 2/2 | 2/2 | 426k | 530s |
| qwen3.8 | 16/16 | 2/2 | 2/2 | 561k | 667s |
| grok-4.5 | 16/16 | 2/2 | 2/2 | N/A | N/A |

### 7.2 Critic 盲审排名（排除 gpt）

| 排名 | 模型 | 总分 | GT 命中 | 耗时 | 误报 |
|---:|---|---:|---|---:|---:|
| 1 | kimi-for-coding | 92.3 | GT1,2,3 | 1332s | 0 |
| 1 | doubao-seed-evolving | 92.3 | GT1,2,3 | 1354s | 0 |
| 3 | doubao-seed-2.0-pro | 90.0 | GT1,3 | 68s | 0 |
| - | LongCat-2.0 | 47.8 | **仅 GT2** | 2735s | 0 |

### 7.3 Reviewer 排名（排除 gpt）

| 排名 | 模型 | Supplemental | 性能中位数 | cross_hashability |
|---:|---|---:|---:|---|
| 1 | kimi-for-coding | 8/8 | 152.5 ms | ✓ |
| 2 | doubao-seed-evolving | 8/8 | 79.8 ms | ✓ |
| 3 | qwen3.8 | 7/8 | 112.1 ms | ✗ |

### 7.4 长任务严格榜（排除 gpt）

| 排名 | 模型 | Strict milestones | Coverage |
|---:|---|---:|---:|
| 1 | qwen3.8 | 8/10 | 0.85 |
| 2 | kimi-for-coding | 5/10 | 0.55 |
| 3 | glm-5.2 (修订) | 5/10 | 0.55 |

### 7.5 省钱模式成本对比

| 模型 | 短 B token | 短 B 分数 | 可修复缺陷数 |
|---|---:|---:|---:|
| mimo-v2.5-pro | 190k | 14/16 | 2（critic 可发现） |
| step-3.7-flash | 327k | 16/16 | 0（有计划时满分） |
| glm-5.2 | 426k | 16/16 | 0 |
| qwen3.8 | 561k | 16/16 | 0 |

## 8. 注意事项

1. **Profile 生效**：自定义 profile 需要 `/new` 或重启 session 后加载
2. **工具限制是硬约束**：code-critic 的 Edit 禁用由工具层执行，不靠 prompt 约束
3. **binding_slot 与 subagent_type 独立**：profile 控制行为，slot 控制模型，可自由组合
4. **Critic 速度**：gemini-3.6-flash 仅 133s（比 evolving/kimi 快 10 倍），doubao-2.0-pro 68s 最快但漏 GT2，两者可根据场景选择
5. **doubao-2.0-pro 稳定性**：复测显示其 critic 行为不稳定（有时全中 GT，有时出误报），适合预筛不适合终审
6. **长任务 Gate 问题**：benchmark hash 校验在文件复制后可能不一致（Windows 行尾差异），导致 Gate indeterminate；这不是模型质量问题
7. **Token 数据缺失**：evolving 和 grok-4.5 的 token 数据为 N/A（后台任务无 usage），成本估算时需注意
8. **LongCat 缓存经济学**：短任务缓存命中率极低（~1.6%），不省钱；但大上下文场景理论命中率 92%，作为额外 critic 后台异步运行时近免费。LongCat 正确性审查不可靠（未命中 GT1），只采纳其性能/资源类 finding
9. **LongCat 不做 coder**：虽然缓存免费，但初始质量低（长任务 3/10），多轮 critic 修复的成本超过 qwen3.8 一次过的成本
