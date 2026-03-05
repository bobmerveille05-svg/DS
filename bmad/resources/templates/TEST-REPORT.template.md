# ==============================================
# TEST-REPORT : {{STRATEGY_NAME}}
# Version      : {{VERSION}}
# Date         : {{DATE}}
# Source       : SOURCE-CODE v{{VERSION}}
# BMAD Phase   : 4 - TEST
# ==============================================

## LEVEL 1 - UNIT TESTS (LOGIC)

### 1.1 Indicator tests

| Test ID | Description | Input | Expected | Actual | PASS/FAIL |
|---------|-------------|-------|----------|--------|-----------|
| TU-01 | [RSI(14) fixed series] | [series] | [value] | [value] | PASS |

### 1.2 Signal tests

| Test ID | Scenario | Expected signal | Actual | PASS/FAIL |
|---------|----------|-----------------|--------|-----------|
| TS-01 | [LONG-1 + LONG-2 true] | LONG | LONG | PASS |

### 1.3 Filter tests

| Test ID | Filter | Condition | Expected | Actual | PASS/FAIL |
|---------|--------|-----------|----------|--------|-----------|
| TF-01 | FLT-1 time | hour=10 in range | PASS | PASS | PASS |

### 1.4 Position sizing tests

| Test ID | Balance | Risk% | SL distance | Expected lots | Actual | PASS/FAIL |
|---------|---------|-------|-------------|---------------|--------|-----------|
| TR-01 | 10000 | 1.0 | 50 pips | 0.20 | 0.20 | PASS |

Summary Level 1:
- Total: [N]
- Passed: [N]
- Failed: [N]

## LEVEL 2 - INTEGRATION TESTS (BEHAVIOR)

### 2.1 Scenarios

| Scenario ID | Description | Expected trades | Actual trades | Match |
|-------------|-------------|----------------|--------------|-------|
| SC-01 | Clear uptrend | 3 LONG | 3 LONG | YES |

### 2.2 State machine verification

| Transition | Expected | Actual | PASS/FAIL |
|------------|----------|--------|-----------|
| IDLE -> IN_LONG | position opened | position opened | PASS |

## LEVEL 3 - STATISTICAL BACKTEST

### 3.1 Configuration

| Parameter | Value |
|----------|-------|
| Platform | [MT4/MT5/TradingView] |
| Symbol | [EURUSD] |
| Timeframe | [H1] |
| Period | [YYYY-MM-DD -> YYYY-MM-DD] |
| Initial capital | [10000] |
| Tick model | [Every tick / ...] |
| Spread | [Real/Variable/Fixed] |
| Commission | [value] |

### 3.2 Mandatory metrics

| Metric | Value | BMAD threshold | PASS/FAIL |
|--------|-------|----------------|-----------|
| Net profit | [value] | > 0 | [PASS/FAIL] |
| Profit factor | [value] | > 1.30 | [PASS/FAIL] |
| Sharpe | [value] | > 1.00 | [PASS/FAIL] |
| Sortino | [value] | > 1.50 | [PASS/FAIL] |
| Max DD % | [value] | < 30% | [PASS/FAIL] |
| Expectancy | [value] | > 0 | [PASS/FAIL] |
| Recovery factor | [value] | > 2.00 | [PASS/FAIL] |
| Total trades | [value] | > 200 | [PASS/FAIL] |

## LEVEL 4 - ROBUSTNESS

### 4.1 Walk-forward analysis
- IS window: [..]
- OOS window: [..]
- Steps: [..]

### 4.2 Monte Carlo
- Runs: [>= 1000]
- Method: [trade permutation / ...]

### 4.3 Parameter sensitivity (+/- 20%)

| Parameter | -20% PF | Default PF | +20% PF | Stable? |
|----------|---------|------------|---------|---------|
| P-01 | [..] | [..] | [..] | [YES/NO] |

### 4.4 Degradation tests

| Degraded condition | Net profit | PF | DD% | Survivable |
|-------------------|-----------|----|-----|------------|
| Baseline | [..] | [..] | [..] | YES |
| Spread +50% | [..] | [..] | [..] | [YES/NO] |

---
STATUS : DRAFT / REVIEW / APPROVED
GATE-04 : PENDING / PASS / FAIL

Gate 04 checklist (required = all true):
- [ ] G04-C01 Unit tests pass 100%
- [ ] G04-C02 Backtest covers >= 5 years OR >= 1000 trades
- [ ] G04-C03 All mandatory metrics computed
- [ ] G04-C04 Walk-forward completed
- [ ] G04-C05 Monte Carlo completed (>= 1000 runs)
- [ ] G04-C06 Parameter sensitivity completed
- [ ] G04-C07 Spread/slippage degradation completed
