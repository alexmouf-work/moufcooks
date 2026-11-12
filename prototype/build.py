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
# The deployed site serves its own fonts from ../fonts, so no visitor's request goes to a font service.
LATIN = "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
LATIN_EXT = "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF"
face = lambda family, weight, file, rng: f"@font-face {{ font-family: '{family}'; font-style: normal; font-weight: {weight}; font-display: swap; src: url(fonts/{file}) format('woff2'); unicode-range: {rng}; }}\n"
fonts = ('<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/literata-latin.woff2">\n'
         '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/josefin-sans-600-latin.woff2">\n<style>\n'
         + face("Josefin Sans", 600, "josefin-sans-600-latin-ext.woff2", LATIN_EXT) + face("Josefin Sans", 600, "josefin-sans-600-latin.woff2", LATIN)
         + face("Literata", "400 600", "literata-latin-ext.woff2", LATIN_EXT) + face("Literata", "400 600", "literata-latin.woff2", LATIN) + "</style>")
head, swapped = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">', lambda m: fonts, head)
assert swapped == 1, "the font stylesheet link was not found in the template"
for f in re.findall(r"url\(fonts/([^)]+)\)", fonts):
    assert (here.parent / "fonts" / f).exists(), f"missing font file: {f}"
(here.parent / "index.html").write_text(
    '<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<meta name="description" content="A family recipe book: recipes to read and follow, one step at a time.">\n'
    '<meta name="theme-color" content="#7A1F2B">\n'
    "<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
    + head + '</head>\n<body>\n<div id="app">' + body + "\n</body>\n</html>\n")
print(len(page))
