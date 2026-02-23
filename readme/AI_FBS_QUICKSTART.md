# AI + FBS Trading Quickstart

This guide explains how to use the SET third-party module:

- `modules/fbs_ai_assistant.py`

The module is designed for **FBS broker trading via MetaTrader 5**.
It does three steps:

1. Pulls market candles from MT5.
2. Builds a base signal (EMA20/EMA50 + RSI14).
3. Optionally uses AI as a confirmation layer before placing an order.

> Important: the default mode is **dry-run** so no real order is sent unless you confirm and disable dry-run.

## 1) Requirements

Install MetaTrader 5 Python package:

```bash
pip3 install MetaTrader5
```

The module also uses:

- `requests` (already used in this repository)

## 2) Optional environment variables

### MT5 / FBS connection

- `FBS_MT5_LOGIN`
- `FBS_MT5_PASSWORD`
- `FBS_MT5_SERVER`
- `FBS_MT5_PATH` (optional terminal path)

### Trading defaults

- `FBS_SYMBOL` (default: `XAUUSD`)
- `FBS_TIMEFRAME` (default: `M15`)
- `FBS_BARS` (default: `250`)
- `FBS_RISK_PCT` (default: `1.0`)
- `FBS_SL_POINTS` (default: `500`)
- `FBS_TP_POINTS` (default: `1000`)
- `FBS_DEVIATION` (default: `20`)
- `FBS_DRY_RUN` (default: `y`)
- `FBS_AI_MIN_CONFIDENCE` (default: `0.65`)

### AI layer (optional)

- `AI_API_KEY`
- `AI_BASE_URL` (default: `https://api.openai.com/v1`)
- `AI_MODEL` (default: `gpt-4o-mini`)

## 3) Run from SET

1. Start SET.
2. Go to `Third Party Modules`.
3. Select `AI Assistant for FBS Trading (MetaTrader 5)`.
4. Fill in your MT5 account details.
5. Review indicator signal and AI confirmation.
6. Confirm order only if you want to proceed.

## 4) Risk notice

- This module is a helper, not guaranteed profit.
- Always test in demo account first.
- You are fully responsible for risk, broker rules, and legal compliance.
