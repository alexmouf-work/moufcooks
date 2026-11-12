import json, re, subprocess, sys
from pathlib import Path
here = Path(__file__).parent
data = subprocess.run([sys.executable, "-I", str(here / "parse.py"), sys.argv[1] if len(sys.argv) > 1 else str(here.parent / "recipes")], capture_output=True, text=True, check=True).stdout
recipes = json.loads(data)
page = (here / "template.html").read_text().replace("__DATA__", json.dumps(recipes, ensure_ascii=False).replace("</", "<\\/"))
out = here / "out"; out.mkdir(exist_ok=True)
(out / "MoufCooks.html").write_text(page)
(out / "preview.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + page + "</body></html>")
# The deployed site: one complete document at the repository root, which is what the host serves.
head, body = page.split('<div id="app">', 1)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
(here.parent / "index.html").write_text(
    '<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<meta name="description" content="A family recipe book: recipes to read and follow, one step at a time.">\n'
    '<meta name="theme-color" content="#7A1F2B">\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    "<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
    + head + '</head>\n<body>\n<div id="app">' + body + "\n</body>\n</html>\n")
print(len(page))
