"""Parse MoufCooks recipe Markdown into the JSON the prototype page embeds."""
import html
import json
import re
import sys
from pathlib import Path

# What the Markdown doesn't carry yet: a kind, a card line and short meta. In the real build these move into
# front matter at the top of each recipe file.
EXTRA = {
    "beef-cheek-ragu": ("Italian", "Slow-braised beef cheek in red wine and tomato, with roasted bone marrow.", "About 7 hours", "Serves 6–8", 6, "people"),
    "coq-au-vin": ("French", "Chicken braised in red wine and cognac, with crisp skin and pickled shallots.", "About 5 hours", "Serves 6–8", 6, "people"),
    "chilli-miso-ramen": ("Japanese", "Creamy chilli miso broth, crisp chicken and soy eggs.", "About 3 hours", "Serves 4", 4, "people"),
    "spatchcock-chicken-kettle": ("American", "A whole chicken roasted over charcoal, with crisp golden skin.", "About 3½ hours", "Serves 4", 4, "people"),
    "pumpkin-spice-syrup": ("American", "A spiced syrup made with real pumpkin, for lattes in minutes.", "About 1 hour", "Makes 350 ml", 10, "lattes"),
}
ORDER = list(EXTRA)


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s.strip()


def blocks(lines):
    """Paragraphs and bullet lists → HTML. Soft-wrapped lines join; indented lines continue a bullet."""
    out, para, items = [], [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        if items:
            out.append("<ul>" + "".join("<li>" + inline(i) + "</li>" for i in items) + "</ul>")
        para, items = [], []

    table = []

    def flush_table():
        nonlocal table
        if table:
            rows = [[inline(c.strip()) for c in r.strip().strip("|").split("|")] for r in table if not re.match(r"\s*\|[\s|:-]+\|\s*$", r)]
            out.append('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows[1:]) + "</tbody></table></div>")
        table = []

    for ln in lines:
        if ln.lstrip().startswith("|"):
            flush()
            table.append(ln)
            continue
        flush_table()
        if not ln.strip():
            flush()
        elif re.match(r"\s*\d+\. ", ln):
            if para:
                flush()
            items.append(re.sub(r"^\s*\d+\. ", "", ln))
        elif re.match(r"\s*[-*] ", ln):
            if para:
                flush()
            items.append(re.sub(r"^\s*[-*] ", "", ln))
        elif items and ln.startswith("  "):
            items[-1] += " " + ln.strip()
        else:
            if items:
                flush()
            para.append(ln.strip())
    flush()
    flush_table()
    return "".join(out)


def parse(path):
    slug = path.stem
    text = path.read_text()
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip()
    # intro: first paragraph after the title
    i = 1
    while not lines[i].strip():
        i += 1
    intro = []
    while lines[i].strip() and not lines[i].startswith("- "):
        intro.append(lines[i].strip())
        i += 1
    # split into H2 sections
    sections, cur = {}, None
    for ln in lines:
        m = re.match(r"## (.+)", ln)
        if m:
            cur = m.group(1).strip()
            sections[cur] = []
        elif cur:
            sections[cur].append(ln)

    # ingredients
    groups, g = [], None
    for ln in sections.get("Shopping list", []):
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", ln)
        if m and not ln.startswith("- "):
            name = m.group(1).rstrip(":")
            if name.lower().startswith(("kit", "to serve")):
                g = None
                continue
            g = {"name": name, "items": []}
            groups.append(g)
        elif ln.startswith("- ") and g is not None:
            g["items"].append(inline(ln[2:]))
        elif ln.startswith("  ") and g is not None and g["items"]:
            g["items"][-1] += " " + inline(ln.strip())
    groups = [x for x in groups if x["items"]]

    # steps, from every "Method…" section, in order
    steps = []
    for name, body in sections.items():
        if not name.startswith("Method"):
            continue
        phase = name.split(":", 1)[1].strip().capitalize() if ":" in name else ""
        cur_step = None
        for ln in body:
            h3 = re.match(r"### (.+)", ln)
            if h3:
                phase = h3.group(1).strip()
                cur_step = None
                continue
            m = re.match(r"\*\*(\d+)\. (.+?)\*\*\s*(.*)", ln)
            if m:
                head = m.group(2).strip()
                rest = m.group(3)
                # "**3. Do the thing** for an hour." → the bold part is the title only when it ends a sentence
                runs_on = bool(rest) and rest[0].islower()
                step_title = re.split(r",| \(| for | at | until ", head)[0] if runs_on else head
                cur_step = {"n": len(steps) + 1, "phase": phase, "title": step_title.rstrip(".:,"),
                            "_do": ([head + " " + rest] if runs_on else ([rest] if rest else [])), "_why": []}
                cur_step["_mode"] = "do"
                steps.append(cur_step)
                continue
            if cur_step is None:
                continue
            if re.match(r"\*Why[^*]*\*", ln):
                cur_step["_mode"] = "why"
                ln = re.sub(r"^\*Why([^*]*)\*\s*", lambda k: ("<<" + k.group(1).strip(" :") + ">> " if k.group(1).strip(" :") else ""), ln)
            elif re.match(r"\*[A-Z][^*]*[:?]\*", ln):  # other italic asides (*Small pieces?*, *Salting:*) read as why-notes
                cur_step["_mode"] = "why"
            cur_step["_" + cur_step["_mode"]].append(ln)
        # tidy
    for s in steps:
        s["text"] = blocks(s.pop("_do"))
        why = blocks(s.pop("_why"))
        why = re.sub(r"&lt;&lt;(.+?)&gt;&gt; ", r"<strong>\1:</strong> ", why)
        why = re.sub(r"(<p>|</strong> )([a-z])", lambda k: k.group(1) + k.group(2).upper(), why)
        s["why"] = re.sub(r"<strong>([a-z])", lambda k: "<strong>" + k.group(1).upper(), why)
        s.pop("_mode")

    skip = ("Shopping list", "Cook's notes")
    extras = [{"name": n, "html": blocks([l for l in b if not l.startswith("### ")])} for n, b in sections.items()
              if n not in skip and not n.startswith("Method")]
    kind, line, time, serves, base, unit = EXTRA[slug]
    return {"slug": slug, "title": title, "intro": inline(" ".join(intro)), "kind": kind, "line": line, "time": time,
            "serves": serves, "base": base, "unit": unit, "groups": groups, "steps": steps, "extras": extras}


if __name__ == "__main__":
    src = Path(sys.argv[1])
    recipes = [parse(src / f"{slug}.md") for slug in ORDER]
    json.dump(recipes, sys.stdout, ensure_ascii=False)
