#!/usr/bin/env python3
"""Mobile-friendly web app for Chance multi-agent analysis."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Sequence

try:
    from tools.chance_agency_agents import (
        AIPredictorAgent,
        AgencyProfileAgent,
        BacktestAgent,
        DataCollectorAgent,
        FeatureAnalystAgent,
        PortfolioBuilderAgent,
        ProfileRegistry,
    )
except ImportError:
    from chance_agency_agents import (
        AIPredictorAgent,
        AgencyProfileAgent,
        BacktestAgent,
        DataCollectorAgent,
        FeatureAnalystAgent,
        PortfolioBuilderAgent,
        ProfileRegistry,
    )


HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="theme-color" content="#1f6feb" />
  <link rel="manifest" href="/manifest.webmanifest" />
  <title>Chance AI Mobile</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f2f4f7; color: #111; }
    .wrap { max-width: 860px; margin: 0 auto; padding: 16px; }
    .card { background: #fff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    h1 { font-size: 22px; margin: 8px 0 14px; }
    h2 { font-size: 17px; margin: 0 0 10px; }
    label { display: block; font-size: 13px; margin: 8px 0 4px; color: #333; }
    textarea, input { width: 100%; box-sizing: border-box; border: 1px solid #ccc; border-radius: 8px; padding: 10px; font-size: 14px; }
    textarea { min-height: 140px; font-family: monospace; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .row4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .actions3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
    button { background: #1f6feb; color: #fff; border: 0; border-radius: 9px; padding: 12px 14px; font-size: 15px; width: 100%; margin-top: 10px; }
    button.secondary { background: #1f2937; }
    button.success { background: #0f9d58; }
    input[type="file"] { background: #fff; padding: 9px; }
    pre { white-space: pre-wrap; word-break: break-word; margin: 0; font-size: 13px; line-height: 1.45; }
    .muted { color: #666; font-size: 12px; }
    @media (max-width: 600px) { .row, .row4, .actions, .actions3 { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Chance AI Mobile</h1>
    <div class="card">
      <h2>Install app</h2>
      <p class="muted">Install this web app to your home screen for one-tap access.</p>
      <button id="installBtn" type="button" class="success">Install to Home Screen</button>
      <p class="muted" id="installHint">If install dialog does not open, use browser menu: Add to Home screen.</p>
    </div>
    <div class="card">
      <h2>1) Paste history CSV</h2>
      <p class="muted">Header example: spade,heart,diamond,club,draw_id</p>
      <textarea id="historyCsv" placeholder="Paste CSV with header..."></textarea>
      <div class="actions">
        <button id="saveHistoryBtn" type="button" class="secondary">Save history locally</button>
        <button id="loadHistoryBtn" type="button" class="success">Load saved history</button>
      </div>
      <div class="row">
        <div>
          <label>Columns (optional, comma-separated)</label>
          <input id="columns" value="spade,heart,diamond,club" />
        </div>
        <div>
          <label>Exclude columns (comma-separated)</label>
          <input id="excludeColumns" value="draw_id,datetime,date,time" />
        </div>
      </div>
    </div>

    <div class="card">
      <h2>2) Add latest draw (optional)</h2>
      <div class="row4">
        <input id="s1" placeholder="Spade" />
        <input id="s2" placeholder="Heart" />
        <input id="s3" placeholder="Diamond" />
        <input id="s4" placeholder="Club" />
      </div>
      <label>Append target columns</label>
      <input id="appendCols" value="spade,heart,diamond,club" />
      <div class="actions3">
        <input id="photoInput" type="file" accept="image/*" capture="environment" />
        <button id="scanPhotoBtn" type="button" class="secondary">Scan from photo (OCR)</button>
        <button id="clearLatestBtn" type="button" class="secondary">Clear latest draw</button>
      </div>
      <p class="muted">Tip: capture only the 4 result cards for best OCR accuracy.</p>
    </div>

    <div class="card">
      <h2>3) Run AI analysis</h2>
      <div class="row">
        <div>
          <label>Top AI lines</label>
          <input id="topAi" type="number" value="10" />
        </div>
        <div>
          <label>Backtest last draws</label>
          <input id="backtestLast" type="number" value="12" />
        </div>
      </div>
      <div class="row">
        <div>
          <label>Double lines</label>
          <input id="doubleLines" type="number" value="3" />
        </div>
        <div>
          <label>Backup lines</label>
          <input id="backupLines" type="number" value="4" />
        </div>
      </div>
      <button id="runBtn">Analyze</button>
    </div>

    <div class="card">
      <h2>Result</h2>
      <button id="copyTicketBtn" type="button" class="secondary">Copy ticket</button>
      <pre id="out">No analysis yet.</pre>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
  <script>
    const out = document.getElementById('out');
    const installBtn = document.getElementById('installBtn');
    let deferredInstallPrompt = null;
    let lastTicketText = '';
    const VALID_VALUES = new Set(['A', 'K', 'Q', 'J', '10', '9', '8', '7']);

    const saveHistory = () => {
      localStorage.setItem('chance_history_csv', document.getElementById('historyCsv').value || '');
      localStorage.setItem('chance_columns', document.getElementById('columns').value || '');
      localStorage.setItem('chance_exclude_columns', document.getElementById('excludeColumns').value || '');
      localStorage.setItem('chance_append_cols', document.getElementById('appendCols').value || '');
      out.textContent = 'History saved locally on this device.';
    };

    const loadHistory = () => {
      document.getElementById('historyCsv').value = localStorage.getItem('chance_history_csv') || '';
      document.getElementById('columns').value = localStorage.getItem('chance_columns') || 'spade,heart,diamond,club';
      document.getElementById('excludeColumns').value = localStorage.getItem('chance_exclude_columns') || 'draw_id,datetime,date,time';
      document.getElementById('appendCols').value = localStorage.getItem('chance_append_cols') || 'spade,heart,diamond,club';
      out.textContent = 'Saved history loaded.';
    };

    const copyTicket = async () => {
      if (!lastTicketText) {
        out.textContent = 'No ticket generated yet. Run analysis first.';
        return;
      }
      try {
        await navigator.clipboard.writeText(lastTicketText);
        out.textContent = out.textContent + '\\n\\nTicket copied to clipboard.';
      } catch (err) {
        out.textContent = out.textContent + '\\n\\nCopy failed. You can copy manually from the result.';
      }
    };

    const normalizeValueToken = (raw) => {
      if (!raw) return null;
      const token = String(raw).toUpperCase().replace(/[^A-Z0-9]/g, '');
      if (!token) return null;
      if (VALID_VALUES.has(token)) return token;
      if (['IO', 'I0', '1O', '10', 'LO', 'L0', 'TO', 'T0'].includes(token)) return '10';
      if (['O', '0'].includes(token)) return '10';
      if (['A', 'K', 'Q', 'J', '9', '8', '7'].includes(token)) return token;
      return null;
    };

    const extractDrawFromWords = (words) => {
      const candidates = [];
      for (const word of words || []) {
        const bits = String(word.text || '').split(/[^A-Za-z0-9]+/).filter(Boolean);
        for (const bit of bits) {
          const token = normalizeValueToken(bit);
          if (!token || !VALID_VALUES.has(token)) continue;
          const bbox = word.bbox || {};
          const x = ((bbox.x0 || 0) + (bbox.x1 || 0)) / 2;
          const y = ((bbox.y0 || 0) + (bbox.y1 || 0)) / 2;
          const conf = Number(word.confidence || 0);
          candidates.push({ token, x, y, conf });
        }
      }
      if (candidates.length < 4) return [];

      const buckets = new Map();
      const bucketSize = 60;
      for (const item of candidates) {
        const key = Math.round(item.y / bucketSize);
        if (!buckets.has(key)) buckets.set(key, []);
        buckets.get(key).push(item);
      }

      let best = [];
      let bestScore = -1;
      for (const items of buckets.values()) {
        if (items.length < 4) continue;
        const avgConf = items.reduce((sum, row) => sum + row.conf, 0) / items.length;
        const score = items.length * 100 + avgConf;
        if (score > bestScore) {
          bestScore = score;
          best = items;
        }
      }

      const chosen = (best.length >= 4 ? best : candidates)
        .slice()
        .sort((a, b) => a.x - b.x)
        .map((row) => row.token);
      return chosen.slice(0, 4);
    };

    const extractDrawFromText = (text) => {
      const bits = String(text || '').split(/[^A-Za-z0-9]+/).filter(Boolean);
      const values = [];
      for (const bit of bits) {
        const token = normalizeValueToken(bit);
        if (token && VALID_VALUES.has(token)) values.push(token);
      }
      return values.slice(0, 4);
    };

    const setLatestDrawFields = (values) => {
      if (!values || values.length !== 4) return;
      document.getElementById('s1').value = values[0];
      document.getElementById('s2').value = values[1];
      document.getElementById('s3').value = values[2];
      document.getElementById('s4').value = values[3];
    };

    const clearLatestDraw = () => {
      document.getElementById('s1').value = '';
      document.getElementById('s2').value = '';
      document.getElementById('s3').value = '';
      document.getElementById('s4').value = '';
      out.textContent = 'Latest draw fields cleared.';
    };

    const scanPhoto = async () => {
      const fileInput = document.getElementById('photoInput');
      const file = fileInput.files && fileInput.files[0];
      if (!file) {
        out.textContent = 'Please choose or capture a photo first.';
        return;
      }
      if (!window.Tesseract) {
        out.textContent = 'OCR engine was not loaded. Please refresh and try again.';
        return;
      }

      out.textContent = 'Scanning image (OCR)... this can take a few seconds.';
      try {
        const result = await window.Tesseract.recognize(file, 'eng');
        let draw = extractDrawFromWords(result?.data?.words || []);
        if (draw.length < 4) {
          draw = extractDrawFromText(result?.data?.text || '');
        }
        if (draw.length < 4) {
          out.textContent = 'Could not detect 4 values automatically. Try a clearer crop around the cards.';
          return;
        }
        setLatestDrawFields(draw);
        out.textContent = `OCR detected latest draw: ${draw.join(', ')}\\nPlease verify and then press Analyze.`;
      } catch (err) {
        out.textContent = `OCR failed: ${err.message}`;
      }
    };

    document.getElementById('saveHistoryBtn').addEventListener('click', saveHistory);
    document.getElementById('loadHistoryBtn').addEventListener('click', loadHistory);
    document.getElementById('copyTicketBtn').addEventListener('click', copyTicket);
    document.getElementById('scanPhotoBtn').addEventListener('click', scanPhoto);
    document.getElementById('clearLatestBtn').addEventListener('click', clearLatestDraw);

    installBtn.addEventListener('click', async () => {
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        const choice = await deferredInstallPrompt.userChoice;
        if (choice.outcome === 'accepted') {
          out.textContent = 'App installation accepted.';
        } else {
          out.textContent = 'Install canceled.';
        }
        deferredInstallPrompt = null;
        installBtn.disabled = true;
        return;
      }
      out.textContent = 'Install dialog unavailable. Use browser menu: Add to Home screen.';
    });

    window.addEventListener('beforeinstallprompt', (event) => {
      event.preventDefault();
      deferredInstallPrompt = event;
      installBtn.disabled = false;
      document.getElementById('installHint').textContent = 'Tap "Install to Home Screen" to add the app.';
    });

    window.addEventListener('appinstalled', () => {
      out.textContent = 'App installed on home screen successfully.';
      installBtn.disabled = true;
    });

    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js').catch(() => {
          // Silent failure - app still works without offline caching.
        });
      });
    }

    loadHistory();

    document.getElementById('runBtn').addEventListener('click', async () => {
      out.textContent = 'Running...';
      const append = [
        document.getElementById('s1').value.trim(),
        document.getElementById('s2').value.trim(),
        document.getElementById('s3').value.trim(),
        document.getElementById('s4').value.trim(),
      ].filter(Boolean);
      const payload = {
        history_csv: document.getElementById('historyCsv').value,
        columns: document.getElementById('columns').value,
        exclude_columns: document.getElementById('excludeColumns').value,
        append_draw: append.length === 4 ? append : [],
        append_columns: document.getElementById('appendCols').value,
        top_ai: Number(document.getElementById('topAi').value || 10),
        backtest_last: Number(document.getElementById('backtestLast').value || 12),
        double_lines: Number(document.getElementById('doubleLines').value || 3),
        backup_lines: Number(document.getElementById('backupLines').value || 4),
      };

      try {
        const res = await fetch('/analyze', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Request failed');

        const doubles = data.portfolio.double_lines.map((v, i) => `${i+1}. ${v.replaceAll('|', ', ')}`).join('\\n');
        const backups = data.portfolio.backup_lines.map((v, i) => `${i+1}. ${v.replaceAll('|', ', ')}`).join('\\n');
        const aiTop = data.ai_lines.slice(0, 8).map((x, i) => `${i+1}. ${x.values.replaceAll('|', ', ')}  [score=${x.score}]`).join('\\n');
        lastTicketText =
`Double lines:
${doubles}

Backup lines:
${backups}`;
        out.textContent =
`Draws: ${data.features.draw_count}
Top values: ${data.features.top_values.join(', ')}

Backtest:
- exact hit rate: ${(data.backtest.exact_hit_rate*100).toFixed(2)}%
- avg best position matches: ${data.backtest.avg_best_position_matches}/4
- avg best symbol overlap: ${data.backtest.avg_best_symbol_overlap}/4

Double lines:
${doubles}

Backup lines:
${backups}

Top AI lines:
${aiTop}`;
      } catch (err) {
        out.textContent = `Error: ${err.message}`;
      }
    });
  </script>
</body>
</html>
"""


def _parse_csv_list(raw: str | None) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _build_temp_csv_from_payload(payload: Dict[str, Any]) -> Path:
    history_csv = str(payload.get("history_csv", "")).strip()
    if not history_csv:
        raise ValueError("history_csv is required.")

    reader = csv.DictReader(io.StringIO(history_csv))
    rows = list(reader)
    fieldnames = reader.fieldnames or []
    if not fieldnames or not rows:
        raise ValueError("history_csv must include header and at least one data row.")

    append_draw = payload.get("append_draw") or []
    append_columns = _parse_csv_list(str(payload.get("append_columns", "")))
    if append_draw:
        if len(append_draw) != 4:
            raise ValueError("append_draw must include exactly 4 values.")
        if not append_columns:
            raise ValueError("append_columns required when append_draw is provided.")
        if len(append_columns) != len(append_draw):
            raise ValueError("append_columns count must match append_draw count.")
        missing = [column for column in append_columns if column not in fieldnames]
        if missing:
            raise ValueError(f"append_columns not found in CSV header: {missing}")

        appended: Dict[str, str] = {name: "" for name in fieldnames}
        for column, value in zip(append_columns, append_draw):
            appended[column] = str(value).strip().upper()

        if "draw_id" in fieldnames:
            draw_ids = [row.get("draw_id", "").strip() for row in rows if row.get("draw_id", "").strip().isdigit()]
            next_id = int(draw_ids[-1]) + 1 if draw_ids else 1
            appended["draw_id"] = str(next_id)
        rows.append(appended)

    fd, temp_path = tempfile.mkstemp(suffix=".csv", text=True)
    Path(temp_path).unlink(missing_ok=True)
    output = Path(temp_path)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return output


def _normalize_card_tokens(raw_text: str) -> List[str]:
    normalized = raw_text.upper()
    for old, new in (
        ("♠", " "),
        ("♥", " "),
        ("♦", " "),
        ("♣", " "),
        ("\n", " "),
        ("\r", " "),
        ("|", " "),
        (",", " "),
    ):
        normalized = normalized.replace(old, new)

    replacements = {
        "A": "A",
        "K": "K",
        "Q": "Q",
        "J": "J",
        "10": "10",
        "0": "10",  # common OCR error for 10
        "T": "10",
        "9": "9",
        "8": "8",
        "7": "7",
    }
    tokens: List[str] = []
    for raw in normalized.split():
        token = replacements.get(raw)
        if token in {"A", "K", "Q", "J", "10", "9", "8", "7"}:
            tokens.append(token)
    return tokens


def _ocr_with_tesseract(image_path: Path) -> str:
    result = subprocess.run(
        ["tesseract", str(image_path), "stdout", "-l", "eng", "--psm", "6"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "tesseract OCR failed")
    return result.stdout


def extract_draw_from_image(image_bytes: bytes) -> List[str]:
    fd, temp_path = tempfile.mkstemp(suffix=".png")
    Path(temp_path).unlink(missing_ok=True)
    path = Path(temp_path)
    path.write_bytes(image_bytes)
    try:
        text = _ocr_with_tesseract(path)
        tokens = _normalize_card_tokens(text)
        if len(tokens) < 4:
            raise ValueError(
                f"OCR found only {len(tokens)} card tokens. Make sure the screenshot clearly shows 4 values."
            )
        return tokens[:4]
    finally:
        path.unlink(missing_ok=True)


def analyze_payload(payload: Dict[str, Any], profiles_dir: Path | None) -> Dict[str, Any]:
    csv_path = _build_temp_csv_from_payload(payload)
    try:
        collector = DataCollectorAgent()
        analyst = FeatureAnalystAgent()
        predictor = AIPredictorAgent()
        backtester = BacktestAgent()
        portfolio_builder = PortfolioBuilderAgent()

        columns = _parse_csv_list(str(payload.get("columns", "")))
        exclude_columns = _parse_csv_list(str(payload.get("exclude_columns", "")))
        draws, chosen_columns = collector.run(
            csv_path=csv_path,
            columns=columns or None,
            exclude_columns=exclude_columns or None,
        )

        registry = ProfileRegistry(loaded=[], missing_roles=[])
        if profiles_dir and profiles_dir.exists():
            registry = AgencyProfileAgent().run(base_dir=profiles_dir, strict=False)

        recent_window = str(payload.get("recent_window", "0.3"))
        top_ai = int(payload.get("top_ai", 10))
        ai_position_top_k = int(payload.get("ai_position_top_k", 5))
        ai_half_life = float(payload.get("ai_half_life", 16.0))
        ai_smoothing = float(payload.get("ai_smoothing", 0.15))
        ai_novelty_lookback = int(payload.get("ai_novelty_lookback", 8))
        backtest_last = int(payload.get("backtest_last", 12))
        backtest_top_k = int(payload.get("backtest_top_k", 7))
        double_lines = int(payload.get("double_lines", 3))
        backup_lines = int(payload.get("backup_lines", 4))

        features = analyst.run(draws=draws, recent_window=recent_window)
        ai_lines = predictor.run(
            draws=draws,
            top_ai=top_ai,
            ai_position_top_k=ai_position_top_k,
            ai_half_life=ai_half_life,
            ai_smoothing=ai_smoothing,
            ai_novelty_lookback=ai_novelty_lookback,
            recent_window=recent_window,
        )
        backtest = backtester.run(
            draws=draws,
            evaluate_last=backtest_last,
            top_k=backtest_top_k,
            ai_position_top_k=ai_position_top_k,
            ai_half_life=ai_half_life,
            ai_smoothing=ai_smoothing,
            ai_novelty_lookback=ai_novelty_lookback,
            recent_window=recent_window,
        )
        portfolio = portfolio_builder.run(
            ai_lines=ai_lines,
            recent_draws=draws[-ai_novelty_lookback:],
            double_count=double_lines,
            backup_count=backup_lines,
        )

        return {
            "columns": chosen_columns,
            "profiles": [
                {
                    "role": profile.role,
                    "name": profile.name,
                    "path": profile.path,
                }
                for profile in registry.loaded
            ],
            "features": {
                "draw_count": features.draw_count,
                "line_length": features.line_length,
                "top_values": features.top_values,
                "position_leaders": features.position_leaders,
            },
            "backtest": {
                "evaluated_draws": backtest.evaluated_draws,
                "top_k": backtest.top_k,
                "exact_hit_rate": backtest.exact_hit_rate,
                "avg_best_position_matches": backtest.avg_best_position_matches,
                "avg_best_symbol_overlap": backtest.avg_best_symbol_overlap,
            },
            "ai_lines": [
                {
                    "values": row.values,
                    "score": row.score,
                    "probability": row.probability,
                    "recency_bonus": row.recency_bonus,
                    "transition_bonus": row.transition_bonus,
                    "synergy_bonus": row.synergy_bonus,
                    "seen_before": row.seen_before,
                }
                for row in ai_lines
            ],
            "portfolio": {
                "double_lines": portfolio.double_lines,
                "backup_lines": portfolio.backup_lines,
            },
        }
    finally:
        csv_path.unlink(missing_ok=True)


class Handler(BaseHTTPRequestHandler):
    profiles_dir: Path | None = None

    def _send_raw(
        self,
        status: HTTPStatus,
        body: bytes,
        content_type: str,
    ) -> None:
        self.send_response(status.value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: Dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/" or self.path.startswith("/?"):
            raw = HTML_PAGE.encode("utf-8")
            self._send_raw(HTTPStatus.OK, raw, "text/html; charset=utf-8")
            return
        if self.path == "/manifest.webmanifest":
            manifest = {
                "name": "Chance AI Mobile",
                "short_name": "ChanceAI",
                "start_url": "/",
                "scope": "/",
                "display": "standalone",
                "background_color": "#f2f4f7",
                "theme_color": "#1f6feb",
                "description": "Mobile AI assistant for Chance analysis.",
                "icons": [
                    {
                        "src": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOTIiIGhlaWdodD0iMTkyIiB2aWV3Qm94PSIwIDAgMTkyIDE5MiI+PHJlY3Qgd2lkdGg9IjE5MiIgaGVpZ2h0PSIxOTIiIHJ4PSIyOCIgc3R5bGU9ImZpbGw6IzFmNmZlYiIvPjx0ZXh0IHg9Ijk2IiB5PSIxMDgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIHN0eWxlPSJmb250LXNpemU6NTA7Zm9udC1mYW1pbHk6QXJpYWw7ZmlsbDojZmZmIj5DQTwvdGV4dD48L3N2Zz4=",
                        "sizes": "192x192",
                        "type": "image/svg+xml",
                    }
                ],
            }
            raw = json.dumps(manifest, ensure_ascii=False).encode("utf-8")
            self._send_raw(HTTPStatus.OK, raw, "application/manifest+json; charset=utf-8")
            return
        if self.path == "/service-worker.js":
            service_worker = """
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('chance-ai-mobile-v1').then((cache) => cache.addAll(['/']))
  );
  self.skipWaiting();
});
self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
""".strip()
            raw = service_worker.encode("utf-8")
            self._send_raw(HTTPStatus.OK, raw, "application/javascript; charset=utf-8")
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"ok": True})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/ocr-draw":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                image_bytes = self.rfile.read(length)
                draw = extract_draw_from_image(image_bytes)
                self._send_json(HTTPStatus.OK, {"draw": draw})
            except Exception as exc:  # noqa: BLE001
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        if self.path != "/analyze":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw or "{}")
            result = analyze_payload(payload, profiles_dir=self.profiles_dir)
            self._send_json(HTTPStatus.OK, result)
        except Exception as exc:  # noqa: BLE001
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run mobile web app for Chance AI platform.")
    parser.add_argument("--host", default="0.0.0.0", help="Host binding (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8787, help="Port (default: 8787)")
    parser.add_argument(
        "--agency-profiles-dir",
        default="/workspace/external/agency-agents",
        help="Path to agency-agents profiles directory.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    Handler.profiles_dir = Path(args.agency_profiles_dir) if args.agency_profiles_dir else None
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Chance mobile web app running on http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
