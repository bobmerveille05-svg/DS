//+------------------------------------------------------------------+
//| {{STRATEGY_NAME}}.mq4                                            |
//| BMAD-Trading Method - generated skeleton                         |
//| Source: STRATEGY-SPEC v{{VERSION}} -> LOGIC-MODEL v{{VERSION}}   |
//+------------------------------------------------------------------+
#property copyright "BMAD-Trading Method"
#property version   "{{VERSION}}"
#property strict

// ================================================================
// [HEADER]
// Strategy : {{STRATEGY_NAME}}
// Author   : {{AUTHOR}}
// Date     : {{DATE}}
// ================================================================

// ================================================================
// [INPUTS] (fill from STRATEGY-SPEC section 6)
// ================================================================
input int    InpRsiPeriod       = 14;     // [P-01]
input int    InpEmaPeriod       = 50;     // [P-02]
input int    InpAtrPeriod       = 14;     // [P-03]
input double InpRsiOversold     = 30.0;   // [P-04]
input double InpRsiOverbought   = 70.0;   // [P-05]
input double InpRiskPercent     = 1.0;    // [P-06]
input double InpAtrMultSL       = 2.0;    // [P-07]
input double InpTPRatio         = 3.0;    // [P-08]
input bool   InpUseTrailing     = true;   // [P-09]
input double InpTrailActivation = 1.0;    // [P-10]
input double InpTrailStepPips   = 10.0;   // [P-11]
input int    InpStartHourUTC    = 8;      // [P-12]
input int    InpEndHourUTC      = 20;     // [P-13]
input double InpMaxSpreadPips   = 3.0;    // [P-14]
input int    InpAdxPeriod       = 14;     // [P-15]
input double InpAdxMinimum      = 20.0;   // [P-16]
input int    InpMagicNumber     = 20240101; // [P-17]
input int    InpMaxPositions    = 1;      // [P-18]

// ================================================================
// [GLOBALS]
// ================================================================
enum ENUM_STATE { STATE_IDLE, STATE_IN_LONG, STATE_IN_SHORT };

ENUM_STATE g_state = STATE_IDLE;
datetime   g_lastBarTime = 0;
int        g_ticket = -1;

// ================================================================
// [INIT]
// ================================================================
int OnInit()
{
    g_state = STATE_IDLE;
    g_lastBarTime = 0;
    g_ticket = -1;
    Print("[BMAD-INIT] {{STRATEGY_NAME}} v{{VERSION}}" );
    return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
    Print("[BMAD-DEINIT] reason=", reason);
}

// ================================================================
// [MAIN]
// ================================================================
void OnTick()
{
    if(!IsNewBar()) return;

    // [CL-01] Not enough bars at startup
    int barsRequired = MathMax(InpRsiPeriod, MathMax(InpEmaPeriod, InpAtrPeriod)) + 5;
    if(Bars < barsRequired) return;

    // [INDICATORS]
    double rsiCurr = iRSI(Symbol(), Period(), InpRsiPeriod, PRICE_CLOSE, 1);
    double rsiPrev = iRSI(Symbol(), Period(), InpRsiPeriod, PRICE_CLOSE, 2);
    double emaVal  = iMA(Symbol(), Period(), InpEmaPeriod, 0, MODE_EMA, PRICE_CLOSE, 1);
    double atrVal  = iATR(Symbol(), Period(), InpAtrPeriod, 1);
    double adxVal  = iADX(Symbol(), Period(), InpAdxPeriod, PRICE_CLOSE, MODE_MAIN, 1);

    // [SIGNALS]
    // [LONG-1]
    bool longCond1 = (rsiPrev <= InpRsiOversold) && (rsiCurr > InpRsiOversold);
    // [LONG-2]
    bool longCond2 = (Close[1] > emaVal);
    bool signalLong = longCond1 && longCond2;

    // [SHORT-1]
    bool shortCond1 = (rsiPrev >= InpRsiOverbought) && (rsiCurr < InpRsiOverbought);
    // [SHORT-2]
    bool shortCond2 = (Close[1] < emaVal);
    bool signalShort = shortCond1 && shortCond2;

    // [FILTERS]
    bool filtersOK = CheckFilters(adxVal);

    // [MANAGEMENT]
    ManageOpenPosition(signalLong, signalShort);

    // [EXECUTION]
    if(g_state == STATE_IDLE && filtersOK)
    {
        if(signalLong)  OpenPosition(OP_BUY, atrVal);
        if(signalShort) OpenPosition(OP_SELL, atrVal);
    }
}

// ================================================================
// [FILTERS]
// ================================================================
bool CheckFilters(double adxVal)
{
    // [FLT-1] Time window (server time assumed)
    int h = Hour();
    if(h < InpStartHourUTC || h >= InpEndHourUTC) return false;

    // [FLT-2] Spread
    double spreadPoints = MarketInfo(Symbol(), MODE_SPREAD);
    double pipSize = (Digits == 5 || Digits == 3) ? Point * 10.0 : Point;
    double spreadPips = (spreadPoints * Point) / pipSize;
    if(spreadPips > InpMaxSpreadPips) return false;

    // [FLT-3] ADX
    if(adxVal < InpAdxMinimum) return false;

    // Max positions
    if(CountMyPositions() >= InpMaxPositions) return false;

    return true;
}

// ================================================================
// [EXECUTION]
// ================================================================
void OpenPosition(int orderType, double atrVal)
{
    // TODO: implement lot sizing, SL/TP, and send orders.
    // Keep full traceability: // [P-06], // [P-07], // [P-08], etc.
    Print("[BMAD-TODO] OpenPosition not implemented yet");
}

void ManageOpenPosition(bool signalLong, bool signalShort)
{
    // TODO: implement trailing stop and reverse-signal exits.
    // Keep rule IDs in comments: // [TRAIL], // [EXIT-SIGNAL], // [EXIT-TIMEOUT]
}

// ================================================================
// [UTILS]
// ================================================================
bool IsNewBar()
{
    datetime t = Time[0];
    if(t != g_lastBarTime) { g_lastBarTime = t; return true; }
    return false;
}

int CountMyPositions()
{
    int count = 0;
    for(int i = OrdersTotal() - 1; i >= 0; i--)
    {
        if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
        if(OrderSymbol() != Symbol()) continue;
        if(OrderMagicNumber() != InpMagicNumber) continue;
        count++;
    }
    return count;
}

//+------------------------------------------------------------------+
