# -*- coding: utf-8 -*-
"""Audit: recompute reviewer replay-v2 scores from raw evaluation JSONs and
cross-check every numeric claim used in our two HTML pages against sources.

Note: the reviewer med_check comparison flags subtest_2/subtest_10 as MISMATCH
by design — their performance_median_ms covers only the passing wide_50000
check (deep_50000 timed out, duration 0.0), so it is not comparable to the
deep+wide medians of other candidates. This is a semantics caveat, not a
wrong number; the leaderboard values themselves are correct."""
import json, statistics, csv, io, sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows GBK console chokes on † etc.

ROOT = Path(r"D:/vscode/kimisubagentexplore/subagentbenchmark")
EV = ROOT / "reviewer/results/debug-subagent-v1-replay-v2/evaluations"

# ---- 1. Recompute reviewer scores from raw JSONs ----
recomputed = {}
for f in sorted(EV.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    cand = d["candidate_id"]
    off = d["official"]
    gate = 1 if d["audit"]["passed"] else 0
    crit = sum(t["passed_criteria"] for t in off["task_results"])
    res = sum(1 for r in off["capabilities"]["resource"] if r["passed"])
    sup = d["supplemental"]["passed"]
    sup_total = d["supplemental"]["total"]
    med = d["supplemental"]["performance_median_ms"]
    perf = sorted(c["duration_ms"] for c in d["supplemental"]["checks"]
                  if c["id"] in ("deep_50000", "wide_50000"))
    med_check = round(statistics.median(perf), 3) if perf else None
    fails = [c["id"] for c in d["supplemental"]["checks"] if not c["passed"]]
    recomputed[cand] = dict(gate=gate, crit=crit, res=res, sup=sup,
                            sup_total=sup_total, med=med, med_check=med_check,
                            fails=fails, model=d["model"])

# Expected values from replay-v2 leaderboard.md (what our pages claim)
LB = {  # cand: (strict_rank, gate, crit, res, sup, median)
 "subtest_7":(1,1,16,2,8,151.672), "subtest_4":(2,1,16,2,8,152.541),
 "subtest_6":(3,1,16,2,7,112.138), "subtest_8":(4,1,16,2,7,115.425),
 "subtest_9":(5,1,16,2,7,116.831), "subtest_5":(6,1,16,2,7,117.036),
 "phi_2":(7,1,16,2,7,117.286),     "subtest_3":(8,1,16,2,7,118.536),
 "subtest_12":(9,1,16,2,7,119.739),"subtest_11":(10,1,16,2,7,121.195),
 "subtest_13":(11,1,16,2,7,124.323),"subtest_10":(12,1,16,1,6,61.646),
 "subtest_2":(13,1,16,1,6,63.297), "subtest_1":(14,0,16,2,7,123.907)}

print("== Reviewer replay-v2: recomputed vs leaderboard ==")
ok = True
for cand,(rk,g,c,r,s,m) in LB.items():
    rc = recomputed[cand]
    good = (rc["gate"]==g and rc["crit"]==c and rc["res"]==r
            and rc["sup"]==s and abs(rc["med"]-m)<0.001
            and (rc["med_check"] is None or abs(rc["med_check"]-m)<0.001))
    ok &= good
    flag = "OK " if good else "MISMATCH"
    print(f"{flag} {cand:<11} gate={rc['gate']} crit={rc['crit']} res={rc['res']} "
          f"sup={rc['sup']}/{rc['sup_total']} med={rc['med']} fails={rc['fails']}")
print("REVIEWER ALL MATCH:", ok)

# Verify deterministic strict ordering key reproduces leaderboard ranks
order = sorted(LB, key=lambda c: (-recomputed[c]["gate"], -recomputed[c]["crit"],
                                  -recomputed[c]["res"], -recomputed[c]["sup"],
                                  recomputed[c]["med"]))
derived = {c: i+1 for i, c in enumerate(order)}
rank_ok = all(derived[c]==LB[c][0] for c in LB)
print("REVIEWER STRICT ORDER REPRODUCED:", rank_ok)

# ---- 2. Long-task CSV vs our page claims ----
def read_csv(p):
    txt = p.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(io.StringIO(txt)))
strict = {r["Label"]: r for r in read_csv(ROOT/"closed_loop_v2/supplemental/results/strict-leaderboard.csv")}
lenient = {r["Label"]: r for r in read_csv(ROOT/"closed_loop_v2/supplemental/results/lenient-leaderboard.csv")}

# our claims: label: (strictMS, rawMS, cov, gate, tokens)
LONG = {
 "subtest_6":(8,8,"0.85","True",3575630), "subtest_7_rerun":(6,6,"0.75","True",3080085),
 "subtest_4":(5,5,"0.55","True",3940122), "glm5.2.fix":(5,5,"0.55","True",4332044),
 "subtest_12":(3,3,"0.45","True",1995355),"phi_2":(3,3,"0.35","True",3818532),
 "subtest_2":(2,2,"0.45","True",2607687), "subtest_3":(2,2,"0.3","True",2787709),
 "subtest_8":(2,2,"0.3","True",3213269),  "subtest_11":(2,2,"0.25","True",3367492),
 "subtest_9":(0,4,"0.5","False",897544),  "subtest_13":(0,4,"0.5","False",6221549),
 "subtest_1":(0,3,"0.4","False",5725459), "subtest_10":(0,1,"0.25","False",1285401),
 "subtest_5":(0,0,"0.1","False",1876466)}
print("\n== Long task: page claims vs CSV ==")
ok2 = True
for lab,(sms,rms,cov,gate,tok) in LONG.items():
    r = strict[lab]
    good = (int(r["StrictMilestoneCount"])==sms and int(r["RawMilestoneCount"])==rms
            and float(r["AcceptanceCoverage"])==float(cov)
            and r["InstructionGate"]==gate and int(r["InferenceTokens"])==tok)
    ok2 &= good
    print(("OK " if good else "MISMATCH"), lab, r["StrictMilestoneCount"], r["RawMilestoneCount"],
          r["AcceptanceCoverage"], r["InstructionGate"], r["InferenceTokens"])
print("LONG ALL MATCH:", ok2)
# lenient ranks used in our cards: doubao-2.0-pro #5, mimo-v2.5 #6, LongCat #8
lr = {lab: lenient[lab]["Rank"] for lab in ("subtest_9","subtest_13","subtest_1","subtest_10","subtest_5")}
print("lenient ranks:", lr, "(claims: raw #5/#6/#8/#14/#15)")

# ---- 3. Short task: verify claims in eval cards vs spec-conformant-v2 ----
short_md = (ROOT/"short/results/final-leaderboard-spec-conformant-v2.md").read_text(encoding="utf-8")
SHORT_CLAIMS = [
 # (needle asserted by our pages)
 "| 1 | A07 | GPT/gpt-5.6-luna | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 306,032",
 "| 2 | A14 | volcano/glm-5.2 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 426,426",
 "| 3 | A06 | qwen/qwen3.8-max-preview | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 561,153",
 "| 4 | A04 | kimi-code/kimi-for-coding | 1 | 4/4 | 16/16 | 16/16 | 1/2 | 2/2 | 194,101",
 "| 1 | B13 | mimo/mimo-v2.5 | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 342,149",
 "| 5 | B06 | qwen/qwen3.8-max-preview | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 863,422",
 "| 7 | B07 | GPT/gpt-5.6-luna | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 880,477",
 "| 4 | B04 | kimi-code/kimi-for-coding | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 2/2 | 803,531",
 "| 15 | B12 | mimo/mimo-v2.5-pro | 0 | 0/4 | 0/16 | **15/16** | 2/2 | 2/2 | 190,320",
 "| 14 | B11 | volcano/minimax-m3 | 1 | 3/4 | 12/16 | 12/16 | 2/2 | 1/2 | 647,000",
 "| 11 | A15 | composer/composer-2.5 † | 1 | 2/4 | 14/16 | 14/16 | 1/2 | 1/2 | N/A",
 "| 11 | B15 | composer/composer-2.5 † | 1 | 4/4 | 16/16 | 16/16 | 2/2 | 1/2 | N/A",
 "| volcano/minimax-m3 | A11 → B11 | -2 | 0 | 0 | -606,213",
 "| stepfun/step-3.7-flash | A05 → B05 | +4 | +3 | 0 | -265,105",
 "| mimo/mimo-v2.5-pro | A12 → B12 | +1 | -2 | -1 | -228,702",
]
print("\n== Short task: page claims vs final-leaderboard-spec-conformant-v2.md ==")
ok3 = True
for n in SHORT_CLAIMS:
    hit = n in short_md
    ok3 &= hit
    print(("OK " if hit else "MISSING"), n[:72])
print("SHORT ALL MATCH:", ok3)

# ---- 4. Check the (now fixed) A02/A10 note in charts page ----
charts = (ROOT/"prototype/finalresultpdf/leaderboard-charts.html").read_text(encoding="utf-8")
print("\n== Charts page A02/A10 note check ==")
bad_note = "在严格榜 official=0（execution 不完整）" in charts
print("charts page still claims A02/A10 strict official=0 (want False):", bad_note)
fixed_note = "official=raw，分别 13/16、12/16" in charts
print("charts page carries corrected note (want True):", fixed_note)
print("source strict A actually has: A02 official 13/16 ->", "| 12 | A02 | deepseek/deepseek-v4-flash | 1 | 2/4 | 13/16" in short_md)
print("source strict A actually has: A10 official 12/16 ->", "| 15 | A10 | volcano/doubao-seed-2.0-code | 1 | 1/4 | 12/16" in short_md)
print("source lenient A has Execution=0 for A02 ->", "| 14 | A02 | deepseek/deepseek-v4-flash | 0 | 13/16" in short_md)
