#!/usr/bin/env python3
"""Simple CLI checker based on the WhatsMyName dataset."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from urllib.parse import quote

# Prevent stdlib/imported dependencies from resolving to src/core/ssl package.
SCRIPT_DIR = str(Path(__file__).resolve().parent)
if SCRIPT_DIR in sys.path:
    sys.path.remove(SCRIPT_DIR)
    sys.path.append(SCRIPT_DIR)

import requests

DEFAULT_DATA_URL = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
DEFAULT_TIMEOUT = 8.0
DEFAULT_WORKERS = 20


@dataclass
class CheckResult:
    site_name: str
    category: str
    account_used: str
    url: str
    status: str
    http_code: int | None
    note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a username/email against sites from the WhatsMyName dataset."
    )
    parser.add_argument("query", help="Username or email to search")
    parser.add_argument(
        "--email",
        action="store_true",
        help="Treat query as an email and test email-derived candidates",
    )
    parser.add_argument(
        "--data-source",
        default=DEFAULT_DATA_URL,
        help="Path to wmn-data.json or URL to fetch it from",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Number of concurrent workers (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit number of checked sites (0 = all)",
    )
    parser.add_argument(
        "--category",
        action="append",
        default=[],
        help="Filter category (can be used multiple times)",
    )
    parser.add_argument(
        "--include-invalid",
        action="store_true",
        help="Include sites marked as invalid in data",
    )
    parser.add_argument(
        "--show-misses",
        action="store_true",
        help="Also print sites that were checked but not found",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )
    return parser.parse_args()


def build_account_candidates(query: str, email_mode: bool) -> List[str]:
    if not email_mode:
        return [query]

    if "@" not in query:
        raise ValueError("--email was provided but query is not a valid email address")

    local_part = query.split("@", 1)[0]
    local_part_no_plus = local_part.split("+", 1)[0]

    candidates: List[str] = [query, local_part]
    if local_part_no_plus and local_part_no_plus not in candidates:
        candidates.append(local_part_no_plus)
    return candidates


def load_data(source: str, timeout: float) -> Dict[str, Any]:
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, timeout=timeout)
        response.raise_for_status()
        return response.json()
    with Path(source).expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sanitize_username(username: str, strip_chars: str | None) -> str:
    if not strip_chars:
        return username
    cleaned = username
    for bad_char in strip_chars:
        cleaned = cleaned.replace(bad_char, "")
    return cleaned


def build_target_url(site: Dict[str, Any], username: str) -> str:
    pretty = site.get("uri_pretty") or site.get("uri_check", "")
    return pretty.replace("{account}", quote(username, safe=""))


def decide_status(
    response_code: int,
    response_text: str,
    e_code: int,
    m_code: int,
    e_string: str,
    m_string: str,
) -> Tuple[str, str]:
    has_exists_string = bool(e_string) and e_string in response_text
    has_missing_string = bool(m_string) and m_string in response_text

    if response_code == m_code and has_missing_string:
        return "missing", "missing code and marker matched"
    if response_code == e_code and has_exists_string and not has_missing_string:
        return "found", "exists code and marker matched"
    if response_code == m_code and m_code != e_code:
        return "missing", "missing code matched"
    if response_code == e_code and e_code != m_code:
        return "found", "exists code matched"
    if has_missing_string and not has_exists_string:
        return "missing", "missing marker matched"
    if has_exists_string and not has_missing_string:
        return "found", "exists marker matched"
    return "unknown", "no clear match for exists/missing markers"


def _check_single_account(site: Dict[str, Any], account: str, timeout: float) -> CheckResult:
    site_name = site.get("name", "unknown")
    category = site.get("cat", "unknown")
    account_for_site = sanitize_username(account, site.get("strip_bad_char"))
    encoded_account = quote(account_for_site, safe="")
    uri_check = site.get("uri_check", "").replace("{account}", encoded_account)

    if not uri_check.startswith("http://") and not uri_check.startswith("https://"):
        return CheckResult(
            site_name=site_name,
            category=category,
            account_used=account_for_site,
            url=build_target_url(site, account_for_site),
            status="unknown",
            http_code=None,
            note="invalid uri_check",
        )

    headers = dict(site.get("headers", {}))
    method = "POST" if site.get("post_body") else "GET"
    data = None
    if site.get("post_body"):
        data = site["post_body"].replace("{account}", account_for_site)

    try:
        response = requests.request(
            method=method,
            url=uri_check,
            headers=headers,
            data=data,
            timeout=timeout,
            allow_redirects=True,
        )
        status, note = decide_status(
            response_code=response.status_code,
            response_text=response.text,
            e_code=site.get("e_code", 200),
            m_code=site.get("m_code", 404),
            e_string=site.get("e_string", ""),
            m_string=site.get("m_string", ""),
        )
        return CheckResult(
            site_name=site_name,
            category=category,
            account_used=account_for_site,
            url=build_target_url(site, account_for_site),
            status=status,
            http_code=response.status_code,
            note=note,
        )
    except requests.RequestException as exc:
        return CheckResult(
            site_name=site_name,
            category=category,
            account_used=account_for_site,
            url=build_target_url(site, account_for_site),
            status="unknown",
            http_code=None,
            note=f"request error: {exc}",
        )


def check_site(site: Dict[str, Any], accounts: List[str], timeout: float) -> CheckResult:
    first_missing: CheckResult | None = None
    first_unknown: CheckResult | None = None

    for account in accounts:
        result = _check_single_account(site, account, timeout)
        if result.status == "found":
            return result
        if result.status == "missing" and first_missing is None:
            first_missing = result
        if result.status == "unknown" and first_unknown is None:
            first_unknown = result

    if first_missing is not None:
        return first_missing
    if first_unknown is not None:
        return first_unknown

    return CheckResult(
        site_name=site.get("name", "unknown"),
        category=site.get("cat", "unknown"),
        account_used=accounts[0] if accounts else "",
        url=build_target_url(site, accounts[0] if accounts else ""),
        status="unknown",
        http_code=None,
        note="no result produced",
    )


def filter_sites(
    sites: Iterable[Dict[str, Any]],
    include_invalid: bool,
    categories: List[str],
) -> List[Dict[str, Any]]:
    wanted_categories = {c.lower().strip() for c in categories if c.strip()}
    filtered = []
    for site in sites:
        if not include_invalid and site.get("valid") is False:
            continue
        if wanted_categories and site.get("cat", "").lower() not in wanted_categories:
            continue
        filtered.append(site)
    return filtered


def main() -> int:
    args = parse_args()
    try:
        account_candidates = build_account_candidates(args.query, args.email)
    except ValueError as exc:
        print(f"Input error: {exc}")
        return 1

    data = load_data(args.data_source, timeout=args.timeout)
    sites = filter_sites(
        data.get("sites", []),
        include_invalid=args.include_invalid,
        categories=args.category,
    )
    if args.limit > 0:
        sites = sites[: args.limit]

    if not sites:
        print("No sites selected after filtering.")
        return 1

    workers = max(1, min(args.workers, len(sites)))
    results: List[CheckResult] = []

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(check_site, site, account_candidates, args.timeout) for site in sites]
        for future in as_completed(futures):
            results.append(future.result())

    found = sorted((r for r in results if r.status == "found"), key=lambda r: r.site_name.lower())
    missing = sorted((r for r in results if r.status == "missing"), key=lambda r: r.site_name.lower())
    unknown = sorted((r for r in results if r.status == "unknown"), key=lambda r: r.site_name.lower())

    if args.json:
        print(
            json.dumps(
                {
                    "query": args.query,
                    "email_mode": args.email,
                    "account_candidates": account_candidates,
                    "checked_sites": len(results),
                    "found_count": len(found),
                    "missing_count": len(missing),
                    "unknown_count": len(unknown),
                    "found": [r.__dict__ for r in found],
                    "missing": [r.__dict__ for r in missing],
                    "unknown": [r.__dict__ for r in unknown],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    print(f"Query: {args.query}")
    if args.email:
        print(f"Email mode: enabled ({', '.join(account_candidates)})")
    print(f"Checked sites: {len(results)}")
    print(f"Found: {len(found)} | Missing: {len(missing)} | Unknown: {len(unknown)}")
    print("")
    if found:
        print("[FOUND]")
        for item in found:
            print(f"- {item.site_name} ({item.category}) [{item.account_used}] -> {item.url}")
        print("")

    if args.show_misses and missing:
        print("[MISSING]")
        for item in missing:
            print(f"- {item.site_name} ({item.category}) [{item.account_used}] [{item.http_code}]")
        print("")

    if unknown:
        print("[UNKNOWN]")
        for item in unknown[:25]:
            print(f"- {item.site_name} ({item.category}) :: {item.note}")
        if len(unknown) > 25:
            print(f"... and {len(unknown) - 25} more unknown results")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
