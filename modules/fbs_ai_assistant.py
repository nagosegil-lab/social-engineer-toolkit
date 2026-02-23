#!/usr/bin/env python
from __future__ import print_function

import json
import os

import requests

try:
    from getpass import getpass
except ImportError:
    getpass = None

try:
    input = raw_input
except NameError:
    pass

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None


MAIN = "AI Assistant for FBS Trading (MetaTrader 5)"
AUTHOR = "Cursor AI"

DEFAULT_AI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_AI_MODEL = "gpt-4o-mini"
DEFAULT_SYMBOL = "XAUUSD"
DEFAULT_TIMEFRAME = "M5"
DEFAULT_BARS = 300
DEFAULT_MAX_SPREAD_POINTS = 45
DEFAULT_SL_ATR_MULT = 0.8
DEFAULT_TP_ATR_MULT = 1.6
DEFAULT_MIN_RR = 1.5
DEFAULT_SCALP_EMA_FAST = 9
DEFAULT_SCALP_EMA_SLOW = 21
DEFAULT_SCALP_RSI_PERIOD = 7
DEFAULT_PROFILE_PRESET = "xau_scalp_aggressive"

PROFILE_PRESETS = {
    "xau_scalp_aggressive": {
        "symbol": "XAUUSD",
        "timeframe": "M1",
        "bars": 500,
        "risk_pct": 1.25,
        "deviation": 30,
        "max_spread_points": 35,
        "fast_profile": True,
        "ema_fast": 7,
        "ema_slow": 17,
        "rsi_period": 6,
        "sl_atr_mult": 0.55,
        "tp_atr_mult": 1.35,
        "min_rr": 2.0,
        "ai_min_confidence": 0.72,
    },
    "xau_scalp_balanced": {
        "symbol": "XAUUSD",
        "timeframe": "M5",
        "bars": 350,
        "risk_pct": 1.0,
        "deviation": 20,
        "max_spread_points": 45,
        "fast_profile": True,
        "ema_fast": 9,
        "ema_slow": 21,
        "rsi_period": 7,
        "sl_atr_mult": 0.8,
        "tp_atr_mult": 1.6,
        "min_rr": 1.5,
        "ai_min_confidence": 0.65,
    },
}


class FbsAiError(Exception):
    """Custom error for AI/FBS trading module failures."""


def _ask(prompt, default=None):
    if default:
        message = "{} [{}]: ".format(prompt, default)
    else:
        message = "{}: ".format(prompt)
    value = input(message).strip()
    if not value and default is not None:
        return default
    return value


def _ask_secret(prompt, env_value):
    if env_value:
        return env_value

    if getpass:
        value = getpass("{}: ".format(prompt)).strip()
    else:
        value = input("{}: ".format(prompt)).strip()
    return value


def _to_float(value, name):
    try:
        return float(value)
    except ValueError:
        raise FbsAiError("Invalid value for {0}: {1}".format(name, value))


def _to_int(value, name):
    try:
        return int(value)
    except ValueError:
        raise FbsAiError("Invalid value for {0}: {1}".format(name, value))


def _to_bool(value, default=False):
    if value is None:
        return default
    text = str(value).strip().lower()
    if text in ("y", "yes", "true", "1", "on"):
        return True
    if text in ("n", "no", "false", "0", "off"):
        return False
    return default


def _resolve_preset(preset_name):
    key = (preset_name or "").strip().lower()
    if not key or key == "custom":
        return None, "custom"
    preset = PROFILE_PRESETS.get(key)
    if preset is None:
        raise FbsAiError(
            "Unknown preset '{0}'. Use one of: {1} or custom.".format(
                preset_name,
                ", ".join(sorted(PROFILE_PRESETS.keys())),
            )
        )
    return preset, key


def _pick_value(env_name, preset, preset_key, fallback):
    env_value = os.getenv(env_name)
    if env_value is not None and env_value != "":
        return env_value
    if preset and preset_key in preset:
        return preset[preset_key]
    return fallback


def _ema(values, period):
    if len(values) < period:
        raise FbsAiError("Not enough candle data for EMA({0}).".format(period))

    k = 2.0 / (period + 1.0)
    ema_value = sum(values[:period]) / float(period)
    for price in values[period:]:
        ema_value = (price * k) + (ema_value * (1.0 - k))
    return ema_value


def _rsi(values, period=14):
    if len(values) < period + 1:
        raise FbsAiError("Not enough candle data for RSI({0}).".format(period))

    gains = []
    losses = []
    for idx in range(1, period + 1):
        diff = values[idx] - values[idx - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(diff))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    for idx in range(period + 1, len(values)):
        diff = values[idx] - values[idx - 1]
        gain = diff if diff > 0 else 0.0
        loss = abs(diff) if diff < 0 else 0.0
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _atr(highs, lows, closes, period=14):
    if len(closes) < period + 1:
        raise FbsAiError("Not enough candle data for ATR({0}).".format(period))

    true_ranges = []
    for idx in range(1, len(closes)):
        high = highs[idx]
        low = lows[idx]
        prev_close = closes[idx - 1]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        true_ranges.append(tr)

    atr_value = sum(true_ranges[:period]) / float(period)
    for tr in true_ranges[period:]:
        atr_value = ((atr_value * (period - 1)) + tr) / float(period)
    return atr_value


def _map_timeframe(name):
    mapping = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    key = (name or "").upper().strip()
    if key not in mapping:
        raise FbsAiError("Unsupported timeframe: {0}".format(name))
    return mapping[key]


def _build_ai_prompt(symbol, timeframe_name, indicators, last_closes, strategy_name):
    return (
        "You are a conservative scalping risk analyst for FBS/MT5.\n"
        "Strategy: {0}\n"
        "Symbol: {1}\n"
        "Timeframe: {2}\n"
        "Indicators: ema_fast={3:.5f}, ema_slow={4:.5f}, rsi={5:.2f}, atr14={6:.5f}\n"
        "Recent closes: {7}\n\n"
        "Return strict JSON with keys only:\n"
        "{{\"action\":\"buy|sell|hold\",\"confidence\":0-1,\"reason\":\"short\"}}\n"
        "Do not add markdown."
    ).format(
        strategy_name,
        symbol,
        timeframe_name,
        indicators["ema_fast"],
        indicators["ema_slow"],
        indicators["rsi"],
        indicators["atr14"],
        ",".join("{0:.5f}".format(v) for v in last_closes),
    )


def _parse_ai_response(payload):
    choices = payload.get("choices", [])
    if not choices:
        raise FbsAiError("AI response has no choices.")

    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not content:
        raise FbsAiError("AI response has empty content.")
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        # Remove fenced code wrappers if the model returned markdown.
        lines = [line for line in lines if not line.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    return cleaned


def _base_signal(indicators):
    ema_fast = indicators["ema_fast"]
    ema_slow = indicators["ema_slow"]
    rsi_value = indicators["rsi"]

    if ema_fast > ema_slow and 45.0 <= rsi_value <= 70.0:
        return "buy", "EMA fast above EMA slow and RSI supports long."
    if ema_fast < ema_slow and 30.0 <= rsi_value <= 55.0:
        return "sell", "EMA fast below EMA slow and RSI supports short."
    return "hold", "Indicators are not aligned for a clear entry."


def _scalp_signal(indicators):
    ema_fast = indicators["ema_fast"]
    ema_slow = indicators["ema_slow"]
    rsi_value = indicators["rsi"]
    last_close = indicators["last_close"]
    prev_close = indicators["prev_close"]

    long_setup = ema_fast > ema_slow and 55.0 <= rsi_value <= 80.0 and last_close > prev_close
    short_setup = ema_fast < ema_slow and 20.0 <= rsi_value <= 45.0 and last_close < prev_close

    if long_setup:
        return "buy", "Scalp long: trend + momentum + immediate impulse."
    if short_setup:
        return "sell", "Scalp short: trend + momentum + immediate impulse."
    return "hold", "Scalp filters are not aligned."


def _normalize_action(value):
    action = (value or "").strip().lower()
    if action in ("buy", "sell", "hold"):
        return action
    return "hold"


def ai_decision(ai_api_key, ai_model, user_prompt, ai_base_url):
    url = ai_base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": "Bearer " + ai_api_key,
        "Content-Type": "application/json",
    }
    data = {
        "model": ai_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a conservative scalping risk analyst.",
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            timeout=60,
        )
    except requests.RequestException as exc:
        raise FbsAiError("Failed to reach AI endpoint: {0}".format(exc))

    if response.status_code >= 400:
        raise FbsAiError(
            "AI request failed ({0}): {1}".format(response.status_code, response.text)
        )

    try:
        payload = response.json()
    except ValueError:
        raise FbsAiError("AI response is not valid JSON.")

    content = _parse_ai_response(payload)
    try:
        decision = json.loads(content)
    except ValueError:
        raise FbsAiError("AI response is not valid JSON content: {0}".format(content))

    action = _normalize_action(decision.get("action"))
    confidence = decision.get("confidence", 0)
    reason = decision.get("reason", "")
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    return {
        "action": action,
        "confidence": max(0.0, min(1.0, confidence)),
        "reason": str(reason).strip(),
    }


def _round_volume(symbol_info, volume):
    min_lot = symbol_info.volume_min
    max_lot = symbol_info.volume_max
    step = symbol_info.volume_step
    if step <= 0:
        raise FbsAiError("Symbol volume step is invalid.")

    if volume < min_lot:
        volume = min_lot
    if volume > max_lot:
        volume = max_lot

    steps = round((volume - min_lot) / step)
    rounded = min_lot + (steps * step)
    return round(rounded, 2)


def _calc_volume_by_risk(account_info, symbol_info, risk_pct, sl_points):
    if sl_points <= 0:
        raise FbsAiError("Stop loss points must be above zero.")

    tick_value = symbol_info.trade_tick_value
    tick_size = symbol_info.trade_tick_size
    point = symbol_info.point

    if tick_value <= 0 or tick_size <= 0 or point <= 0:
        raise FbsAiError("Symbol risk parameters are invalid (tick value/size/point).")

    risk_amount = account_info.balance * (risk_pct / 100.0)
    sl_price_move = sl_points * point
    loss_per_lot = (sl_price_move / tick_size) * tick_value
    if loss_per_lot <= 0:
        raise FbsAiError("Cannot compute loss per lot.")

    raw_volume = risk_amount / loss_per_lot
    return _round_volume(symbol_info, raw_volume)


def _fetch_candles(symbol, timeframe, bars):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None or len(rates) == 0:
        raise FbsAiError("No candle data returned for symbol/timeframe.")

    return {
        "opens": [float(row["open"]) for row in rates],
        "highs": [float(row["high"]) for row in rates],
        "lows": [float(row["low"]) for row in rates],
        "closes": [float(row["close"]) for row in rates],
    }


def _build_indicators(market, ema_fast, ema_slow, rsi_period):
    closes = market["closes"]
    highs = market["highs"]
    lows = market["lows"]
    return {
        "ema_fast": _ema(closes, ema_fast),
        "ema_slow": _ema(closes, ema_slow),
        "rsi": _rsi(closes, rsi_period),
        "atr14": _atr(highs, lows, closes, 14),
        "last_close": closes[-1],
        "prev_close": closes[-2],
    }


def _spread_points(symbol):
    tick = mt5.symbol_info_tick(symbol)
    info = mt5.symbol_info(symbol)
    if tick is None or info is None or info.point <= 0:
        raise FbsAiError("Could not compute spread for symbol: {0}".format(symbol))
    return (tick.ask - tick.bid) / info.point


def _quick_sl_tp_points(indicators, symbol_info, sl_mult, tp_mult, min_rr):
    if sl_mult <= 0 or tp_mult <= 0:
        raise FbsAiError("ATR multipliers must be above zero.")
    if min_rr <= 0:
        raise FbsAiError("Minimum R:R must be above zero.")
    if symbol_info.point <= 0:
        raise FbsAiError("Symbol point is invalid for ATR conversion.")

    atr_points = int(max(1, round(indicators["atr14"] / symbol_info.point)))
    sl_points = int(max(1, round(atr_points * sl_mult)))
    tp_points = int(max(1, round(atr_points * tp_mult)))

    rr = float(tp_points) / float(sl_points)
    if rr < min_rr:
        tp_points = int(max(tp_points, round(sl_points * min_rr)))
        rr = float(tp_points) / float(sl_points)

    return sl_points, tp_points, rr


def _build_order_request(symbol, side, volume, sl_points, tp_points, deviation):
    tick = mt5.symbol_info_tick(symbol)
    symbol_info = mt5.symbol_info(symbol)
    if tick is None or symbol_info is None:
        raise FbsAiError("Could not load tick/symbol info for {0}.".format(symbol))

    point = symbol_info.point
    if point <= 0:
        raise FbsAiError("Symbol point value is invalid.")

    if side == "buy":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
        sl = price - (sl_points * point)
        tp = price + (tp_points * point)
    elif side == "sell":
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
        sl = price + (sl_points * point)
        tp = price - (tp_points * point)
    else:
        raise FbsAiError("Unsupported order side: {0}".format(side))

    filling_mode = symbol_info.filling_mode
    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 240226,
        "comment": "fbs_ai_assistant",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling_mode,
    }


def _place_trade(symbol, side, volume, sl_points, tp_points, deviation, dry_run):
    request = _build_order_request(symbol, side, volume, sl_points, tp_points, deviation)
    if dry_run:
        return {
            "dry_run": True,
            "request": request,
        }

    try:
        result = mt5.order_send(request)
    except Exception as exc:
        raise FbsAiError("Order send failed: {0}".format(exc))

    if result is None:
        raise FbsAiError("Order send returned no result.")
    return result


def _print_banner():
    print("\n--------------------------------------------------")
    print(" AI Assistant for FBS Trading (MetaTrader 5)")
    print("--------------------------------------------------\n")
    print("Fast profile: quick entries/exits for scalping.")
    print("It filters with spread control + optional AI.\n")


def main():
    _print_banner()

    if mt5 is None:
        print("[!] MetaTrader5 module is missing.")
        print("[!] Install with: pip3 install MetaTrader5")
        input("\nPress <enter> to continue")
        return

    preset_name = _ask(
        "Preset (xau_scalp_aggressive/xau_scalp_balanced/custom)",
        os.getenv("FBS_PROFILE_PRESET", DEFAULT_PROFILE_PRESET),
    )
    try:
        preset, preset_key = _resolve_preset(preset_name)
    except FbsAiError as exc:
        print("\n[!] {0}".format(exc))
        input("\nPress <enter> to continue")
        return

    print("\n[*] Active preset: {0}".format(preset_key))

    symbol = _ask(
        "Symbol",
        _pick_value("FBS_SYMBOL", preset, "symbol", DEFAULT_SYMBOL),
    ).upper()
    timeframe_name = _ask(
        "Timeframe (M1/M5/M15/M30/H1/H4/D1)",
        _pick_value("FBS_TIMEFRAME", preset, "timeframe", DEFAULT_TIMEFRAME),
    ).upper()
    bars = _to_int(
        _ask("Number of candles", str(_pick_value("FBS_BARS", preset, "bars", DEFAULT_BARS))),
        "bars",
    )
    risk_pct = _to_float(
        _ask("Risk percent per trade", str(_pick_value("FBS_RISK_PCT", preset, "risk_pct", "1.0"))),
        "risk percent",
    )
    deviation = _to_int(
        _ask("Slippage/deviation", str(_pick_value("FBS_DEVIATION", preset, "deviation", "20"))),
        "deviation",
    )
    max_spread_points = _to_float(
        _ask(
            "Max spread points",
            str(_pick_value("FBS_MAX_SPREAD_POINTS", preset, "max_spread_points", DEFAULT_MAX_SPREAD_POINTS)),
        ),
        "max spread points",
    )

    fast_default = _to_bool(_pick_value("FBS_FAST_PROFILE", preset, "fast_profile", True), default=True)
    fast_profile = _to_bool(
        _ask("Fast scalp profile? (y/n)", "y" if fast_default else "n"),
        default=True,
    )

    ema_fast_period = _to_int(
        _ask(
            "EMA fast period",
            str(_pick_value("FBS_EMA_FAST", preset, "ema_fast", DEFAULT_SCALP_EMA_FAST)),
        ),
        "ema fast period",
    )
    ema_slow_period = _to_int(
        _ask(
            "EMA slow period",
            str(_pick_value("FBS_EMA_SLOW", preset, "ema_slow", DEFAULT_SCALP_EMA_SLOW)),
        ),
        "ema slow period",
    )
    rsi_period = _to_int(
        _ask(
            "RSI period",
            str(_pick_value("FBS_RSI_PERIOD", preset, "rsi_period", DEFAULT_SCALP_RSI_PERIOD)),
        ),
        "rsi period",
    )

    sl_atr_mult = _to_float(
        _ask(
            "SL ATR multiplier",
            str(_pick_value("FBS_SL_ATR_MULT", preset, "sl_atr_mult", DEFAULT_SL_ATR_MULT)),
        ),
        "sl atr multiplier",
    )
    tp_atr_mult = _to_float(
        _ask(
            "TP ATR multiplier",
            str(_pick_value("FBS_TP_ATR_MULT", preset, "tp_atr_mult", DEFAULT_TP_ATR_MULT)),
        ),
        "tp atr multiplier",
    )
    min_rr = _to_float(
        _ask(
            "Minimum risk-reward",
            str(_pick_value("FBS_MIN_RR", preset, "min_rr", DEFAULT_MIN_RR)),
        ),
        "minimum risk-reward",
    )

    manual_sl_points = None
    manual_tp_points = None
    if not fast_profile:
        manual_sl_points = _to_int(
            _ask("Stop loss points", os.getenv("FBS_SL_POINTS", "500")),
            "stop loss points",
        )
        manual_tp_points = _to_int(
            _ask("Take profit points", os.getenv("FBS_TP_POINTS", "1000")),
            "take profit points",
        )

    login_text = _ask("MT5 login", os.getenv("FBS_MT5_LOGIN", ""))
    password = _ask_secret("MT5 password", os.getenv("FBS_MT5_PASSWORD"))
    server = _ask("MT5 server", os.getenv("FBS_MT5_SERVER", ""))
    mt5_path = _ask("MT5 terminal path (optional)", os.getenv("FBS_MT5_PATH", ""))
    dry_run = _to_bool(
        _ask("Dry run only? (y/n)", os.getenv("FBS_DRY_RUN", "y")),
        default=True,
    )

    if not login_text or not password or not server:
        print("\n[!] MT5 login, password and server are required.")
        input("\nPress <enter> to continue")
        return
    if bars < max(60, ema_slow_period + 10):
        print("\n[!] Number of candles is too low for your indicator setup.")
        input("\nPress <enter> to continue")
        return
    if ema_fast_period <= 0 or ema_slow_period <= 0 or ema_fast_period >= ema_slow_period:
        print("\n[!] EMA fast must be > 0 and lower than EMA slow.")
        input("\nPress <enter> to continue")
        return
    if rsi_period < 2:
        print("\n[!] RSI period must be at least 2.")
        input("\nPress <enter> to continue")
        return
    if risk_pct <= 0:
        print("\n[!] Risk percent must be above zero.")
        input("\nPress <enter> to continue")
        return
    if max_spread_points <= 0:
        print("\n[!] Max spread points must be above zero.")
        input("\nPress <enter> to continue")
        return
    if sl_atr_mult <= 0 or tp_atr_mult <= 0 or min_rr <= 0:
        print("\n[!] ATR multipliers and minimum risk-reward must be above zero.")
        input("\nPress <enter> to continue")
        return
    if not fast_profile and (manual_sl_points <= 0 or manual_tp_points <= 0):
        print("\n[!] Stop loss and take profit points must be above zero.")
        input("\nPress <enter> to continue")
        return

    use_ai = _to_bool(_ask("Use AI confirmation layer? (y/n)", "y"), default=True)
    ai_api_key = ""
    ai_model = DEFAULT_AI_MODEL
    ai_base_url = DEFAULT_AI_BASE_URL
    min_ai_confidence = _to_float(
        str(_pick_value("FBS_AI_MIN_CONFIDENCE", preset, "ai_min_confidence", "0.65")),
        "minimum AI confidence",
    )

    if use_ai:
        ai_base_url = _ask("AI base URL", os.getenv("AI_BASE_URL", DEFAULT_AI_BASE_URL))
        ai_model = _ask("AI model", os.getenv("AI_MODEL", DEFAULT_AI_MODEL))
        ai_api_key = _ask_secret("AI API key", os.getenv("AI_API_KEY"))
        min_ai_confidence = _to_float(
            _ask("Minimum AI confidence (0-1)", str(min_ai_confidence)),
            "minimum AI confidence",
        )
        if min_ai_confidence < 0 or min_ai_confidence > 1:
            print("\n[!] Minimum AI confidence must be between 0 and 1.")
            input("\nPress <enter> to continue")
            return

    try:
        login = int(login_text)
    except ValueError:
        print("\n[!] MT5 login must be numeric.")
        input("\nPress <enter> to continue")
        return

    try:
        tf = _map_timeframe(timeframe_name)

        if mt5_path.strip():
            ok = mt5.initialize(path=mt5_path.strip(), login=login, password=password, server=server)
        else:
            ok = mt5.initialize(login=login, password=password, server=server)

        if not ok:
            raise FbsAiError("MT5 initialize failed: {0}".format(mt5.last_error()))

        selected = mt5.symbol_select(symbol, True)
        if not selected:
            raise FbsAiError("Could not select symbol: {0}".format(symbol))

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            raise FbsAiError("Could not load symbol info for {0}.".format(symbol))

        market = _fetch_candles(symbol, tf, bars)
        indicators = _build_indicators(
            market=market,
            ema_fast=ema_fast_period,
            ema_slow=ema_slow_period,
            rsi_period=rsi_period,
        )
        spread_now = _spread_points(symbol)

        if fast_profile:
            base_action, base_reason = _scalp_signal(indicators)
            strategy_name = "{0}_fast_scalp".format(preset_key)
            sl_points, tp_points, rr = _quick_sl_tp_points(
                indicators=indicators,
                symbol_info=symbol_info,
                sl_mult=sl_atr_mult,
                tp_mult=tp_atr_mult,
                min_rr=min_rr,
            )
        else:
            base_action, base_reason = _base_signal(indicators)
            strategy_name = "{0}_standard_signal".format(preset_key)
            sl_points = manual_sl_points
            tp_points = manual_tp_points
            rr = float(tp_points) / float(sl_points)

        print("\n[+] Indicator snapshot")
        print("    EMA{0}: {1:.5f}".format(ema_fast_period, indicators["ema_fast"]))
        print("    EMA{0}: {1:.5f}".format(ema_slow_period, indicators["ema_slow"]))
        print("    RSI{0}: {1:.2f}".format(rsi_period, indicators["rsi"]))
        print("    ATR14: {0:.5f}".format(indicators["atr14"]))
        print("    Spread: {0:.2f} points".format(spread_now))
        print("\n[+] Base signal: {0} ({1})".format(base_action.upper(), base_reason))
        print("[+] Exit profile: SL={0} points, TP={1} points, R:R={2:.2f}".format(
            sl_points, tp_points, rr
        ))

        if spread_now > max_spread_points:
            print(
                "\n[*] Final decision: HOLD (Spread too high: {0:.2f} > {1:.2f})".format(
                    spread_now, max_spread_points
                )
            )
            input("\nPress <enter> to continue")
            return

        final_action = base_action
        final_reason = base_reason

        if use_ai:
            if not ai_api_key:
                raise FbsAiError("AI API key is required when AI layer is enabled.")

            prompt = _build_ai_prompt(
                symbol=symbol,
                timeframe_name=timeframe_name,
                indicators=indicators,
                last_closes=market["closes"][-20:],
                strategy_name=strategy_name,
            )
            decision = ai_decision(
                ai_api_key=ai_api_key,
                ai_model=ai_model,
                user_prompt=prompt,
                ai_base_url=ai_base_url,
            )
            print("\n[+] AI signal: {0} (confidence: {1:.2f})".format(
                decision["action"].upper(),
                decision["confidence"],
            ))
            if decision["reason"]:
                print("    Reason: {0}".format(decision["reason"]))

            # Conservative rule: trade only if base signal and AI agree with enough confidence.
            if decision["action"] == base_action and decision["confidence"] >= min_ai_confidence:
                final_action = base_action
                final_reason = "Base+AI agreement"
            else:
                final_action = "hold"
                final_reason = "No strong agreement between base signal and AI."

        if final_action == "hold":
            print("\n[*] Final decision: HOLD ({0})".format(final_reason))
            input("\nPress <enter> to continue")
            return

        account_info = mt5.account_info()
        if account_info is None:
            raise FbsAiError("Could not fetch account/symbol details for risk sizing.")

        volume = _calc_volume_by_risk(account_info, symbol_info, risk_pct, sl_points)
        print("\n[+] Final decision: {0}".format(final_action.upper()))
        print("    Volume by risk: {0}".format(volume))
        print("    Risk %: {0}".format(risk_pct))
        print("    SL points: {0}".format(sl_points))
        print("    TP points: {0}".format(tp_points))
        print("    Risk-Reward: {0:.2f}".format(rr))
        print("    Dry run: {0}".format("YES" if dry_run else "NO"))

        confirm = _ask("Place order now? (y/n)", "n").lower()
        if confirm != "y":
            print("\n[*] Order cancelled by user.")
            input("\nPress <enter> to continue")
            return

        result = _place_trade(
            symbol=symbol,
            side=final_action,
            volume=volume,
            sl_points=sl_points,
            tp_points=tp_points,
            deviation=deviation,
            dry_run=dry_run,
        )

        if dry_run:
            print("\n[+] Dry-run request preview:")
            print(result["request"])
        else:
            print("\n[+] Trade sent.")
            print("    retcode: {0}".format(result.retcode))
            print("    order:   {0}".format(result.order))
            print("    deal:    {0}".format(result.deal))

    except Exception as exc:
        print("\n[!] {0}".format(exc))
        input("\nPress <enter> to continue")
        return
    finally:
        try:
            mt5.shutdown()
        except Exception:
            pass

    input("\nPress <enter> to continue")
