# ============================================================
# BMAD-TRADING PROOF CERTIFICATE
# Strategy   : {{STRATEGY_NAME}}
# Version    : {{VERSION}}
# Date       : {{DATE}}
# Auditor    : BMAD-AUDITOR
# Decision   : CERTIFIED / CONDITIONAL / REJECTED
# ============================================================

## AXIS 1 - STATISTICAL EDGE (score: [X/4])

| Criterion | Value | Threshold | PASS/FAIL |
|----------|-------|-----------|-----------|
| Expectancy > 0 | [value] | > 0 | [PASS/FAIL] |
| Profit factor > 1.3 | [value] | > 1.30 | [PASS/FAIL] |
| Significance p < 0.05 | [value] | < 0.05 | [PASS/FAIL] |
| Trades > 200 | [value] | > 200 | [PASS/FAIL] |

Significance test:

```
H0: no edge (mean return = 0)
H1: positive edge

Test: [t-test per-trade returns]
t-stat: [..]
p-value: [..]
95% CI: [..]
Conclusion: [reject/do not reject H0]
```

## AXIS 2 - ROBUSTNESS (score: [X/4])

| Criterion | Value | Threshold | PASS/FAIL |
|----------|-------|-----------|-----------|
| WFA efficiency > 50% | [..] | > 50% | [PASS/FAIL] |
| Monte Carlo ruin < 5% | [..] | < 5% | [PASS/FAIL] |
| Sensitivity stable (+/- 20%) | [..] | all stable | [PASS/FAIL] |
| OOS >= 60% of IS | [..] | >= 60% | [PASS/FAIL] |

Overfitting indicator:

```
OOS/IS profit ratio: [..]
Parameter count: [..]
Trades/params: [..]
Overfit risk: LOW / MEDIUM / HIGH
```

## AXIS 3 - RISK (score: [X/4])

| Criterion | Value | Threshold | PASS/FAIL |
|----------|-------|-----------|-----------|
| Max drawdown < 30% | [..] | < 30% | [PASS/FAIL] |
| Recovery factor > 2 | [..] | > 2.00 | [PASS/FAIL] |
| Avg win/avg loss > 1 | [..] | > 1.00 | [PASS/FAIL] |
| Worst month > -10% | [..] | > -10% | [PASS/FAIL] |

Ruin risk analysis (optional):

```
P(ruin) = ((1 - edge) / (1 + edge))^(capital_units)
...
```

## AXIS 4 - CONFORMITY (score: [X/3])

| Criterion | Status | PASS/FAIL |
|----------|--------|-----------|
| Code matches LOGIC-MODEL | verified/not verified | [PASS/FAIL] |
| Edge cases handled | [X/X] | [PASS/FAIL] |
| Traceability complete | complete/incomplete | [PASS/FAIL] |

## AXIS 5 - EXPLOITABILITY (score: [X/3])

| Criterion | Value | Threshold | PASS/FAIL |
|----------|-------|-----------|-----------|
| Spread impact < 20% of profit | [..] | < 20% | [PASS/FAIL] |
| Frequency manageable | [..] | > 3 trades/month | [PASS/FAIL] |
| Executable in real conditions | yes/no | yes | [PASS/FAIL] |

## GLOBAL SCORE

| Axis | Score | Max |
|------|-------|-----|
| Edge | [X] | 4 |
| Robustness | [X] | 4 |
| Risk | [X] | 4 |
| Conformity | [X] | 3 |
| Exploitability | [X] | 3 |
| TOTAL | [X] | 18 |

## FINAL DECISION

```
Decision: CERTIFIED / CONDITIONAL / REJECTED

Conditions (if any):
- Risk per trade <= [..]
- Paper trading for [..] days
- Stop if live DD > [..]
```
