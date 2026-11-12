# Prototype

A working prototype of the site, built from `docs/plans/2026-11-11-site-brief.md`. It is not the site: it exists to
judge the look and the feel before the real build is planned.

- `parse.py` reads the recipes in `../recipes/` into the data the page uses.
- `template.html` is the whole page: styles, markup and behaviour.
- `python3 build.py` writes `../index.html`, the complete page the host serves from the root of the repository. It also
  writes `out/MoufCooks.html` and `out/preview.html`, working copies that are not committed.
- After changing a recipe or the template, run it again and commit `index.html`.

Published copy: https://claude.ai/artifact/Ke8cXbHCit7ksRYd7xwwk2
