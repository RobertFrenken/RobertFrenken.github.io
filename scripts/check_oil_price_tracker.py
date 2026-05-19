#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "_site" / "posts" / "oil_price_tracker.html"


def fail(message: str) -> int:
    print(f"oil-price-tracker smoke test failed: {message}", file=sys.stderr)
    return 1


def assert_contains(text: str, needle: str, message: str) -> None:
    if needle not in text:
        raise AssertionError(message)


def main() -> int:
    if not HTML.exists():
        return fail(f"missing rendered file: {HTML}")

    try:
        rendered = HTML.read_text(encoding="utf-8", errors="replace")
        assert_contains(rendered, 'id="quarto-sidebar"', "sidebar markup missing from rendered HTML")
        assert_contains(rendered, 'id="TOC"', "TOC markup missing from rendered HTML")
        assert_contains(rendered, 'src="../_static/oil_price_tracker_widget.html"', "oil tracker iframe missing from rendered HTML")
        assert_contains(rendered, 'oil_price_tracker_widget.html', "oil tracker widget reference missing from rendered HTML")
    except AssertionError as exc:
        return fail(str(exc))

    print("oil-price-tracker smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
