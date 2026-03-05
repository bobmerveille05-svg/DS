# ==============================================
# LOGIC-MODEL : {{STRATEGY_NAME}}
# Version      : {{VERSION}}
# Date         : {{DATE}}
# Source       : STRATEGY-SPEC v{{VERSION}}
# BMAD Phase   : 2 - LOGIC
# ==============================================

## 1. MATHEMATICAL FORMULAS

### IND-1 : [Indicator name]

Formula:

```
[Exact math formula]
```

Notes:
- Parameters:
- Reference values:

### IND-2 : [Indicator name]

```
[Exact math formula]
```

## 2. STATE MACHINE

States (example):

```
{ IDLE, EVALUATE, IN_LONG, IN_SHORT, COOLDOWN }
```

Transitions (example):

| Current state | Event | Condition | Next state | Action |
|--------------|-------|-----------|------------|--------|
| IDLE | new_bar | signal_long | EVALUATE | - |
| EVALUATE | filters_checked | all_filters_pass(long) | IN_LONG | OPEN_BUY |
| IN_LONG | tick/new_bar | sl_hit | IDLE | CLOSE |

## 3. CANONICAL PSEUDO-CODE (BMAD-PC)

```pseudo
// ============================================================
// BMAD-PC : {{STRATEGY_NAME}}
// Traceability: STRATEGY-SPEC -> LOGIC-MODEL -> this pseudo-code
// ============================================================

INPUTS:
    // [P-01] Example parameter
    input int rsiPeriod = 14  // Range: [5, 50]

GLOBALS:
    state currentState = IDLE

FUNCTION OnNewBar():
    // STEP 1 - Indicators
    // [IND-1]
    rsi = RSI(...)

    // STEP 2 - Signals
    // [LONG-1]
    longCond1 = ...
    // [SHORT-1]
    shortCond1 = ...

    // STEP 3 - Filters
    // [FLT-1]
    filterTime = ...

    // STEP 4 - Manage open position
    IF currentState in {IN_LONG, IN_SHORT}:
        ManageOpenPosition()

    // STEP 5 - Entries
    IF currentState == IDLE:
        IF signalLong AND allFilters:
            OpenPosition(LONG)
            currentState = IN_LONG
        ELIF signalShort AND allFilters:
            OpenPosition(SHORT)
            currentState = IN_SHORT

FUNCTION OpenPosition(direction):
    // [RISK]
    lotSize = CalculateLotSize(riskPercent, slDistance)
    // [SL]
    // [TP]
    SEND_ORDER(...)

FUNCTION ManageOpenPosition():
    // [TRAIL]
    // [EXIT-SIGNAL]
    // [EXIT-TIMEOUT]
    ...
```

## 4. TRUTH TABLE

Provide full combinations for LONG and SHORT.

| Condition set | Filters | Expected signal | Expected action |
|--------------|---------|-----------------|----------------|
| LONG-1..N true | all pass | LONG | OPEN_BUY |
| LONG-1..N true | any fail | NONE | - |

## 5. EDGE CASES

| ID    | Edge case | Expected handling |
|-------|-----------|-------------------|
| CL-01 | Not enough bars at startup | Skip until enough bars |
| CL-02 | Gap beyond SL | Accept slippage, close at market |
| CL-03 | Spread spike | Spread filter blocks entries |
| CL-04 | Long and short at same time | Define priority or neutralize |

---
STATUS : DRAFT / REVIEW / APPROVED
GATE-02 : PENDING / PASS / FAIL

Gate 02 checklist (required = all true):
- [ ] G02-C01 Each indicator has an exact math formula
- [ ] G02-C02 State machine complete (all states + transitions)
- [ ] G02-C03 BMAD-PC covers 100% of the spec
- [ ] G02-C04 Truth table complete
- [ ] G02-C05 Edge cases documented and treated
- [ ] G02-C06 Pseudo-code is platform-agnostic
- [ ] G02-C07 Each rule has an ID traceable to the spec
