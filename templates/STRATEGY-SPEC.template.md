# ==============================================
# STRATEGY-SPEC : {{STRATEGY_NAME}}
# Version      : {{VERSION}}
# Date         : {{DATE}}
# Author       : {{AUTHOR}}
# BMAD Phase   : 1 - CAPTURE
# ==============================================

## 1. IDENTITY

| Field            | Value |
|------------------|-------|
| Name             | {{STRATEGY_NAME}} |
| Class            | [Trend / Mean-Reversion / Breakout / Scalping / ...] |
| Markets          | [EURUSD, GBPUSD, ...] |
| Timeframe(s)     | [M15, H1, H4, ...] |
| Execution type   | [EA auto / Semi-auto / Alert] |

## 2. INDICATORS USED

| ID    | Indicator | Default params | Role (signal/filter) |
|-------|-----------|----------------|----------------------|
| IND-1 | [e.g. RSI] | [period=14, src=close] | [Signal] |
| IND-2 | [e.g. EMA] | [period=50] | [Trend filter] |
| IND-3 | [e.g. ATR] | [period=14] | [SL sizing] |
| IND-4 | [e.g. ADX] | [period=14] | [Trend strength filter] |

## 3. ENTRY CONDITIONS

### 3.1 LONG entry

LONG := (condition_1) AND (condition_2) AND ... AND NOT (exclusion_filter)

| ID     | Condition description | Operator | Reference/value |
|--------|------------------------|----------|-----------------|
| LONG-1 | [e.g. RSI crosses up oversold] | CROSS_UP | [e.g. 30] |
| LONG-2 | [e.g. Close > EMA] | > | EMA(period) |

### 3.2 SHORT entry

SHORT := (condition_1) AND (condition_2) AND ... AND NOT (exclusion_filter)

| ID      | Condition description | Operator | Reference/value |
|---------|------------------------|----------|-----------------|
| SHORT-1 | [e.g. RSI crosses down overbought] | CROSS_DN | [e.g. 70] |
| SHORT-2 | [e.g. Close < EMA] | < | EMA(period) |

### 3.3 Filters

| ID    | Filter | Type |
|-------|--------|------|
| FLT-1 | [e.g. No trade between 22:00-02:00 UTC] | Time |
| FLT-2 | [e.g. Spread <= 3.0 pips] | Execution |
| FLT-3 | [e.g. ADX >= 20] | Technical |

## 4. EXIT CONDITIONS

### 4.1 Stop Loss

| Method | Value/formula |
|--------|---------------|
| [Fixed / ATR / ...] | [e.g. 2.0 * ATR(14)] |

### 4.2 Take Profit

| Method | Value/formula |
|--------|---------------|
| [Fixed / RR ratio / ...] | [e.g. 3.0 * SL distance] |

### 4.3 Trailing Stop

| Activation | Step | Method |
|------------|------|--------|
| [e.g. after +1.0x SL] | [e.g. 10 pips] | [Standard/ATR] |

### 4.4 Other exits

- Exit on reverse signal: [YES/NO]
- Timeout exit: [e.g. close after 48h if neither SL nor TP hit]
- Close on Friday: [YES/NO]

## 5. RISK MANAGEMENT

| Parameter | Value |
|----------|-------|
| Position sizing method | [% equity / fixed / ...] |
| Risk per trade | [e.g. 1.0%] |
| Max open positions | [e.g. 1] |
| Max drawdown allowed | [e.g. 20%] |
| Action when DD max reached | [Stop trading / Reduce size / ...] |

## 6. FULL PARAMETER LIST

| ID   | Name | Type | Default | Min | Max | Description |
|------|------|------|---------|-----|-----|-------------|
| P-01 | rsiPeriod | int | 14 | 5 | 50 | RSI period |
| P-02 | emaPeriod | int | 50 | 10 | 200 | EMA period |
| P-03 | atrPeriod | int | 14 | 5 | 50 | ATR period |
| P-04 | rsiOversold | float | 30.0 | 10.0 | 40.0 | Oversold level |
| P-05 | rsiOverbought | float | 70.0 | 60.0 | 90.0 | Overbought level |
| P-06 | riskPercent | float | 1.0 | 0.1 | 5.0 | Risk per trade (%) |
| P-07 | atrMultSL | float | 2.0 | 0.5 | 5.0 | SL = ATR * mult |
| P-08 | tpRatio | float | 3.0 | 1.0 | 10.0 | TP/SL ratio |
| P-09 | useTrailing | bool | true | - | - | Enable trailing |
| P-10 | trailActivation | float | 1.0 | 0.5 | 3.0 | Activation (x SL) |
| P-11 | trailStepPips | float | 10.0 | 1.0 | 50.0 | Trailing step (pips) |
| P-12 | startHourUTC | int | 8 | 0 | 23 | Trading start hour (UTC) |
| P-13 | endHourUTC | int | 20 | 0 | 23 | Trading end hour (UTC) |
| P-14 | maxSpreadPips | float | 3.0 | 0.0 | 20.0 | Spread limit |
| P-15 | adxPeriod | int | 14 | 5 | 50 | ADX period |
| P-16 | adxMinimum | float | 20.0 | 5.0 | 50.0 | ADX minimum |
| P-17 | magicNumber | int | 20240101 | 1 | 2147483647 | MT4/MT5 magic |
| P-18 | maxPositions | int | 1 | 1 | 20 | Max simultaneous positions |

## 7. OPERATIONAL CONSTRAINTS

| Constraint | Value |
|-----------|-------|
| Trading hours | [e.g. 08:00-20:00 UTC] |
| Excluded days | [e.g. Sunday] |
| Max spread | [e.g. 3.0 pips] |
| Slippage tolerance | [e.g. 2 pips] |
| Broker requirements | [ECN/STP, hedging allowed, ...] |

## 8. PERFORMANCE EXPECTATIONS (trader assumptions)

| Metric | Minimum expectation |
|--------|---------------------|
| Win rate | [e.g. > 45%] |
| Profit factor | [e.g. > 1.5] |
| Max drawdown | [e.g. < 20%] |
| Monthly return | [e.g. 3-5%] |

---
STATUS : DRAFT / REVIEW / APPROVED
GATE-01 : PENDING / PASS / FAIL

Gate 01 checklist (required = all true):
- [ ] G01-C01 All LONG entry conditions listed
- [ ] G01-C02 All SHORT entry conditions listed
- [ ] G01-C03 Stop Loss defined (method + value)
- [ ] G01-C04 Take Profit defined
- [ ] G01-C05 Risk management defined (position sizing)
- [ ] G01-C06 Target markets and timeframes listed
- [ ] G01-C07 All parameters have type/default/range
- [ ] G01-C08 Operational constraints defined
- [ ] G01-C09 Spec is unambiguous (single interpretation)
