#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "_site" / "posts" / "oil_price_tracker.html"
WIDGET = ROOT / "_site" / "_static" / "oil_price_tracker_widget.html"
VEGA = ROOT / "_site" / "_static" / "vendor" / "vega.min.js"
VEGA_LITE = ROOT / "_site" / "_static" / "vendor" / "vega-lite.min.js"
VEGA_EMBED = ROOT / "_site" / "_static" / "vendor" / "vega-embed.min.js"


def fail(message: str) -> int:
    print(f"oil-price-tracker smoke test failed: {message}", file=sys.stderr)
    return 1


def assert_contains(text: str, needle: str, message: str) -> None:
    if needle not in text:
        raise AssertionError(message)


def run_browser_check() -> str:
    chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    if not chrome:
        raise RuntimeError("google-chrome not found on PATH")

    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000", "--directory", str(ROOT / "_site")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1)
        proc = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-cache",
                "--virtual-time-budget=20000",
                "--dump-dom",
                "http://127.0.0.1:8000/_static/oil_price_tracker_widget.html",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "chrome dump-dom failed")
        return proc.stdout
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def main() -> int:
    if not HTML.exists():
        return fail(f"missing rendered file: {HTML}")
    if not WIDGET.exists():
        return fail(f"missing widget file: {WIDGET}")
    if not VEGA.exists():
        return fail(f"missing Vega vendor file: {VEGA}")
    if not VEGA_LITE.exists():
        return fail(f"missing Vega-Lite vendor file: {VEGA_LITE}")
    if not VEGA_EMBED.exists():
        return fail(f"missing Vega Embed vendor file: {VEGA_EMBED}")

    try:
        rendered = HTML.read_text(encoding="utf-8", errors="replace")
        assert_contains(rendered, 'id="quarto-sidebar"', "sidebar markup missing from rendered HTML")
        assert_contains(rendered, 'id="TOC"', "TOC markup missing from rendered HTML")
        assert_contains(rendered, 'src="../_static/oil_price_tracker_widget.html"', "oil tracker iframe missing from rendered HTML")
        browser_dom = run_browser_check()
        assert_contains(browser_dom, 'data-oil-tracker-shell', "oil tracker shell missing from browser-rendered widget")
        assert_contains(browser_dom, 'class="marks"', "Vega canvas missing from browser-rendered widget")
    except AssertionError as exc:
        return fail(str(exc))
    except RuntimeError as exc:
        return fail(str(exc))

    print("oil-price-tracker smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
