#!/usr/bin/env python3
"""Publish the HSGA pages from ../Semantic Architecture/ into the workbench.

Copies each source page to tools/, adds the workbench bridge (theme sync, tabs)
and, for the Explorer, hides its own theme button when embedded. Before a page
is replaced, the copy currently in tools/ is kept in legacy/hsga/ with the date
it was last published. Run after editing a source page:

    python3 ingest/hsga_sync.py
"""
import re, shutil, sys, time
from pathlib import Path

WB = Path(__file__).resolve().parent.parent
SRC = WB.parent / "Semantic Architecture"
PAGES = {  # source file -> (tools/ file, extra adapter CSS)
    "HSGA Explorer — Holonic Semantic Governance Architecture.html":
        ("hsga-explorer.html", "html.ke-embedded #themebtn{display:none!important}"),
    "HSGA Architecture Walkthrough.html": ("hsga-walkthrough.html", ""),
}
HEAD = ('<!-- ke-workbench:head -->\n<link rel="stylesheet" href="../assets/ke-theme.css">\n'
        '<script src="../assets/ke-bridge.js"></script>\n')

def main():
    for name, (dest, css) in PAGES.items():
        src = SRC / name
        if not src.exists():
            print("missing:", src); continue
        html = src.read_text(encoding="utf-8")
        html = re.sub(r"<!-- ke-workbench:head -->.*?<!-- /ke-workbench:head -->\n?", "", html, flags=re.S)
        block = HEAD + (f'<style id="ke-adapter">{css}</style>\n' if css else "") + "<!-- /ke-workbench:head -->\n"
        html, n = re.subn(r"(<head[^>]*>\s*)", lambda m: m.group(1) + block, html, count=1)
        if not n:
            print("no <head> in", name); continue
        out = WB / "tools" / dest
        if out.exists():
            if out.read_text(encoding="utf-8") == html:
                print("unchanged:", dest); continue
            arch = WB / "legacy" / "hsga"; arch.mkdir(parents=True, exist_ok=True)
            stamp = time.strftime("%Y-%m-%d", time.localtime(out.stat().st_mtime))
            shutil.copy2(out, arch / f"{out.stem}-{stamp}{out.suffix}")
        out.write_text(html, encoding="utf-8")
        print("published:", dest)

if __name__ == "__main__":
    sys.exit(main())
