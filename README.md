# MOUFCOOKS

A family recipe book. Alexander and their family each add the recipes they cook, and anyone can read them.

**Status:** a folder of Markdown recipes, and a working prototype of the website. The host serves `index.html` at the
root of this repository; it is generated, so change `prototype/` or a recipe and rebuild rather than editing it.

## The plan

A static website at **cooking.mouftools.com**, for one job: reading and following a recipe.

- **No sign-in of any kind.** Everything is public and read-only. Recipes are added by committing Markdown here.
- **Calm, warm, simple and clean.** Its own look, not MoufTools': large readable type, plenty of space, two fonts only
  (one for titles and subtitles, one for body text).
- **Photos, and later videos, of the steps.** Each step has a slot for a photo or a short video, so they can be added
  recipe by recipe without changing the layout.
- **A cooking view:** one step at a time in large type, for a phone or tablet propped up in the kitchen.
- **Recipes stay Markdown.** The site is built from the files in `recipes/`, so nothing written now is lost.

Mock-up: https://claude.ai/artifact/2yBcy8oUc5vkdigyknTmm9

## Where things are

| Path | What it is |
|---|---|
| [`recipes/`](recipes/) | One Markdown file per recipe. Unsorted for now; it will be organised later. |
| [`index.html`](index.html) | The site as deployed. Generated: run `python3 prototype/build.py` after changing a recipe or the prototype. |
| [`prototype/`](prototype/) | What the site is generated from. |
| [`fonts/`](fonts/) | The two typefaces, served by the site itself, with their open licences. |
| [`pages/`](pages/) | The privacy policy and the terms of use, as Markdown. Edit the words here, then rebuild. |

## Adding a recipe (for now)

Copy an existing file in `recipes/`, name it after the dish in lower case with hyphens (`beef-cheek-ragu.md`), and keep
the same sections: what it is, a shopping list (assume nothing is in the cupboard), two versions, each with a
timeline: **standard** (start to table in one day) and **elevated** (the longer timeframe, a day or two ahead, for
deeper flavour), method (with why each step matters), serving, leftovers (how it keeps and what to turn it
into next), notes.

British English and metric throughout. Oven temperatures give both fan and conventional settings.
