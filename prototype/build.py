import json, re, subprocess, sys
from pathlib import Path
here = Path(__file__).parent
data = subprocess.run([sys.executable, "-I", str(here / "parse.py"), sys.argv[1]], capture_output=True, text=True, check=True).stdout
recipes = json.loads(data)
page = (here / "template.html").read_text().replace("__DATA__", json.dumps(recipes, ensure_ascii=False).replace("</", "<\\/"))
out = here / "out"; out.mkdir(exist_ok=True)
(out / "MoufCooks.html").write_text(page)
(out / "preview.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + page + "</body></html>")
print(len(page))
