# MOUFCOOKS

A family recipe book. Alexander and their family each add the recipes they cook, and anyone can read them.

**Status:** a folder of Markdown recipes for now. The website below is planned, not built.

## The plan

- **Anyone can read.** No login is needed to view a recipe.
- **Family can add.** Adding or editing a recipe needs a Google sign-in. Each family member uses their own account.
- **Looks like MoufTools.** The site follows MoufTools' style: [`alexmouf-work/mouftools`](https://github.com/alexmouf-work/mouftools),
  a single page of translucent glass panels over an all-CSS sunset sea.
- **Borrows from Lemma where it saves time.** [`alexmouf-work/lemma`](https://github.com/alexmouf-work/lemma) already
  has pieces this site needs. These are candidates, not decisions:
  - Google sign-in through Supabase Auth (`src/auth/google.ts`, `src/auth/supabaseClient.ts`, `src/ui/GoogleButton.tsx`).
  - Its public quiz index: public to read, writable when signed in. That is the same shape as this site.
  - Design tokens and small UI parts (`src/styles/tokens.css`, `src/ui/Btn.tsx`, `Header.tsx`, `Icon.tsx`, `Spinner.tsx`).
  - Its habit of keeping every decision in one file (`decisions/DECISIONS.md`).
- **Recipes stay Markdown.** The site will read and write the same Markdown files, so nothing written now is lost.

**Open question for the build:** MoufTools has no build step and uses plain JavaScript. Lemma is Vite, React and
TypeScript. Borrowing Lemma's parts means taking its stack; keeping MoufTools' simplicity means porting only the
ideas.

## Where things are

| Path | What it is |
|---|---|
| [`recipes/`](recipes/) | One Markdown file per recipe. Unsorted for now; it will be organised later. |

## Adding a recipe (for now)

Copy an existing file in `recipes/`, name it after the dish in lower case with hyphens (`beef-cheek-ragu.md`), and keep
the same sections: what it is, a shopping list (assume nothing is in the cupboard), a timeline (recipes are usually
planned a day or two ahead), method (with why each step matters), serving, leftovers (how it keeps and what to turn it
into next), notes.

British English and metric throughout. Oven temperatures give both fan and conventional settings.
