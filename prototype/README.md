# Prototype

A working prototype of the site, built from `docs/plans/2026-11-11-site-brief.md`. It is not the site: it exists to
judge the look and the feel before the real build is planned.

- `parse.py` reads the recipes in `../recipes/` into the data the page uses.
- `template.html` is the whole page: styles, markup and behaviour.
- `python3 build.py ../recipes` writes `out/MoufCooks.html` (the page) and `out/preview.html` (the same, wrapped so a
  browser can open it directly).

Published copy: https://claude.ai/artifact/Ke8cXbHCit7ksRYd7xwwk2
