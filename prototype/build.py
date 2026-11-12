import html, json, re, subprocess, sys
from pathlib import Path
here = Path(__file__).parent
data = subprocess.run([sys.executable, "-I", str(here / "parse.py"), sys.argv[1] if len(sys.argv) > 1 else str(here.parent / "recipes")], capture_output=True, text=True, check=True).stdout
recipes = json.loads(data)

# The plain pages (privacy policy, terms of use): Markdown in ../pages, one "# Title", a "Last updated" line, "## " sections.
sys.path.insert(0, str(here))
from parse import blocks

def doc(path):
    links = []
    def keep(m):
        links.append((m.group(1), m.group(2)))
        return f"@@{len(links) - 1}@@"
    text = re.sub(r"\[([^\]]+)\]\(((?:https?://|mailto:)[^)\s]+)\)", keep, path.read_text())
    title, parts, cur = "", [], []
    for ln in text.splitlines():
        if ln.startswith("# "):
            title = ln[2:].strip()
        elif ln.startswith("## "):
            parts.append(blocks(cur)); cur = []; parts.append("<h2>" + html.escape(ln[3:].strip()) + "</h2>")
        else:
            cur.append(ln)
    parts.append(blocks(cur))
    body = re.sub(r"@@(\d+)@@", lambda m: '<a href="%s"%s>%s</a>' % (html.escape(links[int(m.group(1))][1]), "" if links[int(m.group(1))][1].startswith("mailto:") else ' target="_blank" rel="noopener"', html.escape(links[int(m.group(1))][0])), "".join(parts))
    return {"title": title, "html": body}

docs = {p.stem: doc(p) for p in sorted((here.parent / "pages").glob("*.md"))}
page = (here / "template.html").read_text().replace("__DATA__", json.dumps(recipes, ensure_ascii=False).replace("</", "<\\/")).replace("__PAGES__", json.dumps(docs, ensure_ascii=False).replace("</", "<\\/"))
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
