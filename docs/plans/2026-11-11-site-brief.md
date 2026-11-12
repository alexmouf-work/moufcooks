# MoufCooks site: the brief

The prompt the site is designed and built from. Quoted lines are Alexander's own words.

## What it is
A static website at **cooking.mouftools.com** with one job: "reading and following a recipe". The recipes are the
Markdown files in `recipes/`. There is "no need for sign in of any kind".

## Who it's for
Alexander's family, cooking at home. Design for a middle-aged reader who is not technical, often on a phone or tablet
propped up in the kitchen, with wet or floury hands, glancing between the pan and the screen.

## How it should feel
- "A calm, warm, middle-aged-woman-friendly website. Keep it simple and clean."
- "Completely ignore the mouftools style."
- Simple is not bare: "give the site more detailing and make it prettier."
- Detailing in the manner of "art-deco architecture": sunbursts, stepped (ziggurat) silhouettes, chevrons, strong
  vertical lines, symmetry, double inlay lines, brass against stone.
- "Make it deep red rather than green": oxblood red `#7A1F2B` is the main colour, with brass on warm ivory. (This
  replaces the sage green of the first mock-ups.)
- No logo mark. The name is set in type.
- "Don't use more than two fonts total. One for body text and the other for titles and subtitles."
- "Make it feel *sexy* in terms of how smooth it is to use": every tap answers at once, pages flow into each other,
  nothing jumps or flashes.

## What it must do
1. **Home:** show every recipe with its photo, name, time and servings; let the reader narrow by kind.
2. **The recipe, page by page:** "don't make it a scrollable thing, instead make it a page-by-page thing with arrows
   to progress or return", with "nice appropriate animations between each step". The pages are: the recipe itself,
   what you need (tickable while shopping or cooking), each step with its "why", then serving, leftovers and notes.
   Swipe and arrow keys work too. The screen stays awake, and coming back returns to the same page.
3. **Any number of people:** "add sliders for the number of people". A slider reworks every amount. Where a recipe has
   two versions, **standard** and **elevated**, the reader switches between them.
4. **Photos, and later videos, of the steps:** "we may show photographs or later even videos of the steps, so be sure
   to prepare for that." Each step has a slot that appears when a photo or video exists for it, and the page looks
   finished without any.

## Rules
- Real recipe text only, read from the Markdown. No invented copy; Alexander writes any welcome or about lines.
- On-screen words cut to what a cook needs: names, amounts, actions.
- Large type (body about 19 px or more), high contrast (4.5:1), touch targets of 44 px or more, visible keyboard focus.
- Works at phone width with no sideways scrolling; follows the reader's light or dark setting.
- Motion is calm and purposeful: one orchestrated moment on arrival, otherwise movement only answers the reader's
  action. One easing curve, three durations. Respect "reduce motion".
- No sign-in, no tracking, no build-time dependencies beyond turning Markdown into pages.

## References
- Cooking views: one step visible at a time in large type, an ingredient checklist beside it, and returning the cook
  to their place ([screensdesign.com](https://screensdesign.com/articles/recipe-cooking-mode-step-navigation-ux/),
  [SideChef](https://business.sidechef.com/recipe-platform/ux-best-practices-for-recipe-sites)).
- Keeping the screen awake while cooking: the Screen Wake Lock API, as Betty Crocker's site does
  ([web.dev case study](https://web.dev/case-studies/betty-crocker)).
- Art deco motifs: sunbursts, stepped ziggurat profiles, chevrons and zigzags, vertical emphasis
  ([Docomomo US](https://docomomo-us.org/style/art-deco), [Buffalo Architecture and History](https://buffaloah.com/a/archsty/deco)).

## Done when
- A first-time reader can find a recipe and start cooking it in two taps.
- Every screen reads clearly at 390 px and at 1280 px wide, in light and dark.
- Nothing on screen is there only as decoration that gets in the way of reading.
