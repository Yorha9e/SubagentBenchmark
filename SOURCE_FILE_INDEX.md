# SUBAGENT BENCHMARK — 源文件真实路径映射与审计索引 (Ground-Truth Data Audit)

这份文档详细记录了本实验中所有补充测试模型及基线模型在磁盘上的**真实物理文件路径、文件大小与评估归档位置**。所有数值均可通过底层 Harness 跑场生成的 JSON、CSV 与 MD 文件直接复核，绝非臆造。

---

## 1. 最新补充模型组 (Subtests 11 – 15 实测源文件)

### ✦ grok-4.6 (Subtest 13 / Subagent 独立跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/grok-4.6/results/A01.json` (4,251 bytes) & `B01.json`
- **长任务结果 (Long Task)**:
  `prototype/finalresultpdf/longtaskresult/grok-4.6/results/subtest_1-evaluation.json` (43,372 bytes)
- **Reviewer 调试 (Reviewer Debug)**:
  `prototype/finalresultpdf/reviewerresult/grok-4.6/results/evaluation.json` (7,823 bytes)
- **Critic 盲审 (Critic Audit)**:
  - Candidate A: `prototype/finalresultpdf/criticresult/results/critic-grok-v1/reviews/candidate-A.json` (4,954 bytes)
  - Candidate B: `prototype/finalresultpdf/criticresult/results/critic-grok-v1/reviews/candidate-B.json` (4,891 bytes)

### ✦ ox-openrouter (Subtest 13 / OpenRouter 独立跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/ox-openrouter/results/A01.json` (4,251 bytes) & `B01.json`
- **长任务结果 (Long Task)**:
  `prototype/finalresultpdf/longtaskresult/ox-openrouter/results/subtest_1-evaluation.json` (47,117 bytes)
- **Reviewer 调试 (Reviewer Debug)**:
  `prototype/finalresultpdf/reviewerresult/ox-openrouter/results/evaluation.json` (7,836 bytes)
- **Critic 盲审 (Critic Audit)**:
  - Candidate A: `prototype/finalresultpdf/criticresult/results/critic-ox-openrouter-v1/reviews/candidate-A.json` (4,006 bytes)
  - Candidate B: `prototype/finalresultpdf/criticresult/results/critic-ox-openrouter-v1/reviews/candidate-B.json` (1,815 bytes)

### ✦ muse-spark-1.2 (Subtest 12 / Muse-Spark 极速跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/muse-spark-1.2/results/A01.json` (4,251 bytes)
- **长任务结果 (Long Task)**:
  `prototype/finalresultpdf/longtaskresult/muse-spark-1.2/results/subtest_1-evaluation.json` (44,078 bytes)
- **Reviewer 调试 (Reviewer Debug)**:
  `prototype/finalresultpdf/reviewerresult/results/debug-subagent-v1-replay-v2/evaluations/subtest_12.json` (7,907 bytes)
- **Critic 盲审 (Critic Audit)**:
  `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_12.json` (5,594 bytes)

### ✦ ox-alpha-free (Subtest 13 / OpenRouter Alpha 跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/ox-alpha-free/results/A01.json` (4,251 bytes)
- **长任务结果 (Long Task)**:
  `prototype/finalresultpdf/longtaskresult/ox-alpha-free/results/subtest_1-evaluation.json` (48,268 bytes)
- **Reviewer 调试 (Reviewer Debug)**:
  `prototype/finalresultpdf/reviewerresult/results/debug-subagent-v1-replay-v2/evaluations/subtest_13.json` (7,901 bytes)
- **Critic 盲审 (Critic Audit)**:
  `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_13.json` (4,002 bytes)

### ✦ doubao-seed-evolving (Subtest 11 / Doubao Evolving 跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/doubao-evolving/results/A01.json` (4,251 bytes)
- **Reviewer 调试 (Reviewer Debug)**:
  `prototype/finalresultpdf/reviewerresult/results/debug-subagent-v1-replay-v2/evaluations/subtest_11.json` (7,908 bytes)
- **Critic 盲审 (Critic Audit)**:
  `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_11.json` (1,050 bytes)

### ‡ grok-4.5 (Subtest 14 High Effort 补充跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/supplemental/subtest14-grok-high/results/subtest14-grok-high-report.json` (4,641 bytes)
- **长任务报告 (Long Task)**:
  `prototype/finalresultpdf/longtaskresult/reports/subtest_14-grok-high-report.md` (3,125 bytes)

### § hy3 (Subtest 15 English Prompt 补充跑场)
- **短任务结果 (Short Task)**:
  `prototype/finalresultpdf/shorttaskresult/supplemental/subtest15-english/results/subtest15-english-report.json` (4,622 bytes)
- **长任务报告 (Long Task)**:
  `prototype/finalresultpdf/longtaskresult/reports/subtest_15-hy3-report.md` (2,998 bytes)

---

## 2. 隔离子测试补充模型组 (Subtests 1 – 10 源文件)

| 模型名称 | Subtest ID | Critic 盲审 JSON 路径 | 字节大小 |
|---|---|---|---|
| **`gpt-5.6-sol ✦`** | Subtest 6 | `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_6.json` | 1,861 bytes |
| **`deepseek-v4-pro ✦`** | Subtest 2 | `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_2.json` | 1,027 bytes |
| **`glm-5.3 ✦`** | Subtest 3 | `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_3.json` | 1,689 bytes |
| **`deepseek-v4-flash (v2)`** | Subtest 4 | `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_4.json` | 2,387 bytes |
| **`claude-opus ✦`** | Subtest 5 | `prototype/finalresultpdf/criticresult/results/critic-model-select-v1/reviews/subtest_5.json` | 1,288 bytes |
| **`k3 (low) ✦`** | Subtest 1 | `prototype/finalresultpdf/shorttaskresult/k3-phi1/results/A01.json` | 4,251 bytes |

---

## 3. 全局基准汇总源文件

1. **短任务规格符合性总表**:
   `shorttaskresult/combined-leaderboard/final-leaderboard-spec-conformant-v2-with-subtest14-subtest15.md`
2. **长任务严格与宽松 CSV 总表**:
   - 严格榜: `closed_loop_v2/supplemental/results/strict-leaderboard.csv`
   - 宽松榜: `closed_loop_v2/supplemental/results/lenient-leaderboard.csv`
3. **Reviewer Debug Replay-v2 总表**:
   `reviewerresult/results/debug-subagent-v1-replay-v2/leaderboard.md`
4. **Critic 盲审评分总表**:
   `criticresult/results/critic-model-select-v1/score-summary.json`

---
*此索引文档已落盘，随时可供系统查验与校验。*
