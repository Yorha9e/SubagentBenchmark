# Long-task model output archive

## Purpose

This folder is a copy-only archive of long-task model output records. It does not replace, rewrite, or modify the original frozen benchmark data.

Archived record types:

- `raw-wire/`: raw `wire.jsonl` conversation/usage records copied from the agent session directories;
- `evaluations/`: evaluator JSON and candidate usage metadata for the appended completed runs;
- `reports/`: generated single-model reports for the appended completed runs;
- `attempts/`: stopped, blocked, or superseded attempts retained for audit but excluded from rankings.

## Counted long-task runs

| Archive label | Slot | Model | Effort | Status | Raw record |
|---|---|---|---|---|---|
| `subtest_1_longcat` | subtest_1 | `MT/LongCat-2.0` | high | completed | `raw-wire/subtest_1_longcat/wire.jsonl` |
| `subtest_2_deepseek_flash` | subtest_2 | `deepseek/deepseek-v4-flash` | default | completed | `raw-wire/subtest_2_deepseek_flash/wire.jsonl` |
| `subtest_3_deepseek_pro` | subtest_3 | `deepseek/deepseek-v4-pro` | default | completed | `raw-wire/subtest_3_deepseek_pro/wire.jsonl` |
| `subtest_4_kimi` | subtest_4 | `kimi-code/kimi-for-coding` | default | completed | `raw-wire/subtest_4_kimi/wire.jsonl` |
| `subtest_5_step_flash` | subtest_5 | `stepfun/step-3.7-flash` | high | completed | `raw-wire/subtest_5_step_flash/wire.jsonl` |
| `subtest_6_qwen` | subtest_6 | `qwen/qwen3.8-max-preview` | xhigh | completed | `raw-wire/subtest_6_qwen/wire.jsonl` |
| `subtest_7_gpt_luna_provider_blocked` | subtest_7 | `GPT/gpt-5.6-luna` | max | provider blocked before response | `raw-wire/subtest_7_gpt_luna_provider_blocked/wire.jsonl` |
| `subtest_8_doubao_turbo` | subtest_8 | `volcano/doubao-seed-2.1-turbo` | high | completed | `raw-wire/subtest_8_doubao_turbo/wire.jsonl` |
| `subtest_9_doubao_pro` | subtest_9 | `volcano/doubao-seed-2.0-pro` | high | completed | `raw-wire/subtest_9_doubao_pro/wire.jsonl` |
| `subtest_10_doubao_code` | subtest_10 | `volcano/doubao-seed-2.0-code` | high | completed | `raw-wire/subtest_10_doubao_code/wire.jsonl` |
| `phi_5_fable5` | phi_5 | `CC/claude-fable-5` | high | completed | `raw-wire/phi_5_fable5/wire.jsonl` |
| `phi_6_fable5_max` | phi_6 | `CC/claude-fable-5 (max)` | max | completed | `raw-wire/phi_6_fable5_max/wire.jsonl` |
| `phi_7_sonnet5_max` | phi_7 | `CC/claude-sonnet-5 (max)` | max | completed | `raw-wire/phi_7_sonnet5_max/wire.jsonl` |
| `subtest_14_grok45_high` | subtest_14 | `grok/grok-4.5` | high | completed | `raw-wire/subtest_14_grok45_high/wire.jsonl` |
| `subtest_15_hy3_max` | subtest_15 | `tx/hy3` | max | completed | `raw-wire/subtest_15_hy3_max/wire.jsonl` |

## Appended run results

| Slot | Model | Coverage | Passed | Raw MS | Inference tokens | Metadata |
|---|---|---:|---:|---:|---:|---|
| `phi_5` | `CC/claude-fable-5` | 0.80 | 16/20 | 8/10 | 3,555,161 | `evaluations/phi_5-*`, `reports/phi_5-report.md` |
| `phi_6` | `CC/claude-fable-5 (max)` | 0.85 | 17/20 | 8/10 | 3,986,982 | `evaluations/phi_6-*`, `reports/phi_6-report.md` |
| `phi_7` | `CC/claude-sonnet-5 (max)` | 0.75 | 15/20 | 7/10 | 11,644,395 | `evaluations/phi_7-*`, `reports/phi_7-report.md` |
| `subtest_14` | `grok/grok-4.5 (high)` | 0.75 | 15/20 | 5/10 | 1,651,941 | `evaluations/subtest_14-grok-high-*`, `reports/subtest_14-grok-high-report.md` |
| `subtest_15` | `tx/hy3 (max)` | 0.30 | 6/20 | 2/10 | 5,135,697 | `evaluations/subtest_15-hy3-*`, `reports/subtest_15-hy3-report.md` |

## Excluded attempts

The `attempts/` directory retains raw wire files for audit only. These are not counted as independent leaderboard candidates:

- phi6 `agent-2`: stopped high-effort attempt;
- phi6 `agent-3`: prompt-path error;
- phi6 `agent-5`: provider 502 before completion;
- subtest_14 `agent-8` through `agent-13`: haiku adaptive-thinking provider blocks;
- subtest_14 `agent-14`: earlier Grok medium run, superseded by the requested Grok high run;
- subtest_14 `agent-15`: haiku run stopped before model output.

## Integrity note

All files in this archive were copied from their original locations. The original `closed_loop_v2/`, single-model benchmark copies, evaluator outputs, and frozen leaderboard files were not overwritten by this archive operation.
