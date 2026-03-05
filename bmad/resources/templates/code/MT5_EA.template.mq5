//+------------------------------------------------------------------+
//| {{STRATEGY_NAME}}.mq5                                            |
//| BMAD-Trading Method - generated skeleton                         |
//| Source: STRATEGY-SPEC v{{VERSION}} -> LOGIC-MODEL v{{VERSION}}   |
//+------------------------------------------------------------------+
#property copyright "BMAD-Trading Method"
#property version   "{{VERSION}}"

#include <Trade\Trade.mqh>
#include <Trade\SymbolInfo.mqh>
#include <Trade\AccountInfo.mqh>

// ================================================================
// [HEADER]
// Strategy : {{STRATEGY_NAME}}
// Author   : {{AUTHOR}}
// Date     : {{DATE}}
// ================================================================

// ================================================================
// [INPUTS]
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
input ulong  InpMagicNumber     = 20240101; // [P-17]
input int    InpMaxPositions    = 1;      // [P-18]

// ================================================================
// [GLOBALS]
// ================================================================
enum ENUM_STATE { STATE_IDLE, STATE_IN_LONG, STATE_IN_SHORT };

CTrade      trade;
CSymbolInfo sym;
CAccountInfo acc;

ENUM_STATE  g_state = STATE_IDLE;
datetime    g_lastBar = 0;

int h_rsi = INVALID_HANDLE;
int h_ema = INVALID_HANDLE;
int h_atr = INVALID_HANDLE;
int h_adx = INVALID_HANDLE;

int OnInit()
{
    trade.SetExpertMagicNumber(InpMagicNumber);

    if(!sym.Name(Symbol()))
    {
        Print("[BMAD-ERROR] Symbol init failed");
        return INIT_FAILED;
    }

    h_rsi = iRSI(Symbol(), Period(), InpRsiPeriod, PRICE_CLOSE);
    h_ema = iMA(Symbol(), Period(), InpEmaPeriod, 0, MODE_EMA, PRICE_CLOSE);
    h_atr = iATR(Symbol(), Period(), InpAtrPeriod);
    h_adx = iADX(Symbol(), Period(), InpAdxPeriod);

    if(h_rsi == INVALID_HANDLE || h_ema == INVALID_HANDLE || h_atr == INVALID_HANDLE || h_adx == INVALID_HANDLE)
    {
        Print("[BMAD-ERROR] indicator handle init failed");
        return INIT_FAILED;
    }

    Print("[BMAD-INIT] {{STRATEGY_NAME}} v{{VERSION}}");
    return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
    if(h_rsi != INVALID_HANDLE) IndicatorRelease(h_rsi);
    if(h_ema != INVALID_HANDLE) IndicatorRelease(h_ema);
    if(h_atr != INVALID_HANDLE) IndicatorRelease(h_atr);
    if(h_adx != INVALID_HANDLE) IndicatorRelease(h_adx);
    Print("[BMAD-DEINIT] reason=", reason);
}

void OnTick()
{
    if(!IsNewBar()) return;

    sym.RefreshRates();

    // [INDICATORS]
    double rsiBuf[2], emaBuf[1], atrBuf[1], adxBuf[1];
    if(CopyBuffer(h_rsi, 0, 1, 2, rsiBuf) < 2) return;
    if(CopyBuffer(h_ema, 0, 1, 1, emaBuf) < 1) return;
    if(CopyBuffer(h_atr, 0, 1, 1, atrBuf) < 1) return;
    if(CopyBuffer(h_adx, 0, 1, 1, adxBuf) < 1) return;

    double rsiCurr = rsiBuf[1];
    double rsiPrev = rsiBuf[0];
    double emaVal  = emaBuf[0];
    double atrVal  = atrBuf[0];
    double adxVal  = adxBuf[0];

    // [SIGNALS]
    // [LONG-1]
    bool longCond1 = (rsiPrev <= InpRsiOversold) && (rsiCurr > InpRsiOversold);
    // [LONG-2]
    bool longCond2 = (iClose(Symbol(), Period(), 1) > emaVal);
    bool signalLong = longCond1 && longCond2;

    // [SHORT-1]
    bool shortCond1 = (rsiPrev >= InpRsiOverbought) && (rsiCurr < InpRsiOverbought);
    // [SHORT-2]
    bool shortCond2 = (iClose(Symbol(), Period(), 1) < emaVal);
    bool signalShort = shortCond1 && shortCond2;

    // [FILTERS]
    bool filtersOK = CheckFilters(adxVal);

    // [MANAGEMENT]
    ManagePosition(signalLong, signalShort);

    // [EXECUTION]
    if(g_state == STATE_IDLE && filtersOK)
    {
        if(signalLong)  OpenTrade(ORDER_TYPE_BUY, atrVal);
        if(signalShort) OpenTrade(ORDER_TYPE_SELL, atrVal);
    }
}

bool CheckFilters(double adxVal)
{
    // [FLT-1] Time window
    MqlDateTime dt;
    TimeCurrent(dt);
    if(dt.hour < InpStartHourUTC || dt.hour >= InpEndHourUTC) return false;

    // [FLT-2] Spread
    double pipSize = sym.Point() * ((sym.Digits() == 5 || sym.Digits() == 3) ? 10.0 : 1.0);
    double spreadPips = (double)sym.Spread() * sym.Point() / pipSize;
    if(spreadPips > InpMaxSpreadPips) return false;

    // [FLT-3] ADX
    if(adxVal < InpAdxMinimum) return false;

    if(CountPositions() >= InpMaxPositions) return false;
    return true;
}

void OpenTrade(ENUM_ORDER_TYPE type, double atrVal)
{
    // TODO: implement lot sizing, SL/TP, send via CTrade.
    Print("[BMAD-TODO] OpenTrade not implemented yet");
}

void ManagePosition(bool signalLong, bool signalShort)
{
    // TODO: implement trailing stop and reverse exits.
}

bool IsNewBar()
{
    datetime t = iTime(Symbol(), Period(), 0);
    if(t != g_lastBar) { g_lastBar = t; return true; }
    return false;
}

int CountPositions()
{
    int count = 0;
    for(int i = PositionsTotal() - 1; i >= 0; i--)
    {
        ulong ticket = PositionGetTicket(i);
        if(ticket == 0) continue;
        if(PositionGetInteger(POSITION_MAGIC) != (long)InpMagicNumber) continue;
        if(PositionGetString(POSITION_SYMBOL) != Symbol()) continue;
        count++;
    }
    return count;
}

//+------------------------------------------------------------------+
