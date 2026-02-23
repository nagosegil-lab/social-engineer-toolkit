# AI + FBS Trading Quickstart

This guide explains how to use the SET third-party module:

- `modules/fbs_ai_assistant.py`

The module is designed for **FBS broker trading via MetaTrader 5**.
It does three steps:

1. Pulls market candles from MT5.
2. Builds a fast scalp signal (EMA9/EMA21 + RSI7 + momentum).
3. Uses ATR for quick SL/TP exits and optional AI confirmation.

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

- `FBS_PROFILE_PRESET` (default: `xau_scalp_aggressive`)
- `FBS_SYMBOL` (default: `XAUUSD`)
- `FBS_TIMEFRAME` (default: `M5`)
- `FBS_BARS` (default: `300`)
- `FBS_RISK_PCT` (default: `1.0`)
- `FBS_DEVIATION` (default: `20`)
- `FBS_MAX_SPREAD_POINTS` (default: `45`)
- `FBS_SESSION_MODE` (default: `overlap`)
- `FBS_FAST_PROFILE` (default: `y`)
- `FBS_EMA_FAST` (default: `9`)
- `FBS_EMA_SLOW` (default: `21`)
- `FBS_RSI_PERIOD` (default: `7`)
- `FBS_SL_ATR_MULT` (default: `0.8`)
- `FBS_TP_ATR_MULT` (default: `1.6`)
- `FBS_MIN_RR` (default: `1.5`)
- `FBS_DRY_RUN` (default: `y`)
- `FBS_AI_MIN_CONFIDENCE` (default: `0.65`)

Manual fallback (if `FBS_FAST_PROFILE=n`):

- `FBS_SL_POINTS`
- `FBS_TP_POINTS`

### AI layer (optional)

- `AI_API_KEY`
- `AI_BASE_URL` (default: `https://api.openai.com/v1`)
- `AI_MODEL` (default: `gpt-4o-mini`)

## 3) Run from SET

1. Start SET.
2. Go to `Third Party Modules`.
3. Select `AI Assistant for FBS Trading (MetaTrader 5)`.
4. Fill in your MT5 account details.
5. Keep `Fast scalp profile` enabled for quick entries/exits.
6. Review spread filter, SL/TP from ATR, and AI confirmation.
7. Confirm order only if you want to proceed.

## 4) Presets

Supported values for `FBS_PROFILE_PRESET`:

- `xau_scalp_aggressive` (default): fast and tighter setup for XAUUSD.
- `xau_scalp_balanced`: slower and more conservative than aggressive.
- `custom`: full manual control from prompts / env vars.

Session filter modes:

- `off`
- `overlap` (London/New York overlap, UTC 12:00-16:00)
- `london` (UTC 07:00-16:00)
- `newyork` (UTC 12:00-21:00)
- `london_newyork` (London OR New York session)

Aggressive preset baseline:

- Timeframe `M1`
- EMA `7/17`
- RSI `6`
- SL ATR multiplier `0.55`
- TP ATR multiplier `1.35`
- Min R:R `2.0`
- AI confidence floor `0.72`
- Spread filter `<= 35` points
- Session filter `overlap`

## 5) Risk notice

- This module is a helper, not guaranteed profit.
- Always test in demo account first.
- You are fully responsible for risk, broker rules, and legal compliance.
