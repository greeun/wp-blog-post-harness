#!/usr/bin/env python3
"""Render a self-contained HTML/CSS file to a static PNG via headless Chromium.

This is the editorial-visual render path for the WordPress blog post harness. It
exists so the Generator can hand-design card-news / poster / schematic graphics in
HTML+CSS (full control over type hierarchy, color system, layout) and ship them as
plugin-independent static images — instead of every visual collapsing into the same
auto-generated Mermaid look.

Use Mermaid (`mmdc`) only for genuine node-graph structural diagrams. Use THIS for
everything that benefits from editorial design: concept cards, comparison posters,
labeled schematics, hero/cover cards, numbered step strips, quote cards, etc.

Examples
--------
# Card-news card (4:5, 1080x1350), retina-crisp:
python3 render_html.py card.html -o assets/card_1.png --width 1080 --height 1350 --scale 2

# Capture only a specific element (auto-height), e.g. one .card node:
python3 render_html.py card.html -o assets/card_1.png --selector ".card" --width 1080 --scale 2

# Full-page capture (height grows to content), good for tall infographics:
python3 render_html.py infographic.html -o assets/info_1.png --width 1200 --full-page --scale 2

Requirements
------------
Playwright with Chromium. If `playwright` import fails, install:
    python3 -m pip install --break-system-packages playwright
    python3 -m playwright install chromium

On render failure, the Generator records the error in handoff.md and accepts FAIL —
never fabricate a PNG.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Render self-contained HTML/CSS to PNG (headless Chromium).")
    ap.add_argument("html", help="Path to a self-contained HTML file (inline CSS; web fonts via <link>/@import).")
    ap.add_argument("-o", "--output", required=True, help="Output PNG path.")
    ap.add_argument("--width", type=int, default=1080, help="Viewport width in px (default 1080).")
    ap.add_argument("--height", type=int, default=1350, help="Viewport height in px (default 1350 = 4:5 card). Ignored with --full-page or --selector auto-height.")
    ap.add_argument("--scale", type=float, default=2.0, help="Device scale factor for crisp output (default 2 = retina).")
    ap.add_argument("--selector", default=None, help="CSS selector to screenshot a single element (height auto-fits content).")
    ap.add_argument("--full-page", action="store_true", help="Capture the full scrollable page (height grows to content).")
    ap.add_argument("--wait", type=int, default=400, help="Extra ms to wait after load for fonts/layout (default 400).")
    args = ap.parse_args()

    html_path = Path(args.html).resolve()
    if not html_path.is_file():
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        return 2

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: playwright not installed.\n"
            "  python3 -m pip install --break-system-packages playwright\n"
            "  python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return 3

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--force-color-profile=srgb"])
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        # file:// so relative assets (local images/fonts next to the HTML) resolve.
        page.goto(html_path.as_uri(), wait_until="networkidle")
        try:
            page.wait_for_timeout(args.wait)
        except Exception:
            pass

        shot_kwargs = {"path": str(out_path)}
        if args.selector:
            el = page.query_selector(args.selector)
            if el is None:
                print(f"ERROR: selector not found: {args.selector}", file=sys.stderr)
                browser.close()
                return 4
            el.screenshot(path=str(out_path))
        else:
            if args.full_page:
                shot_kwargs["full_page"] = True
            page.screenshot(**shot_kwargs)
        browser.close()

    size = os.path.getsize(out_path)
    print(f"RENDERED: {out_path} ({size} bytes, {args.width}px @ {args.scale}x)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
