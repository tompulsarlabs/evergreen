---
id: 2026-08-31-tomgreenai-photo-01
type: build
state: open
repo: tompulsarlabs/tomgreen.ai
lane: workhorse
pool: anthropic
created: 2026-08-31T17:05:00+02:00
created_by: tom
expires: 2026-09-07T17:05:00+02:00
budget: { wall_minutes: 25 }
---

## Task

Remove Tom's profile photo from the site. His face belongs on LinkedIn; the
site should carry proof of work instead.

**Start by establishing what actually exists.** PR #10 (merged
2026-09-01 12:17 CEST, "One object, two layers") describes PersonalHero as
carrying "a portrait slot that holds its own aspect box so adding the
photograph later shifts nothing" — so the site may hold a reserved *empty
slot* rather than a rendered photo, and some items below may not apply.
Remove the slot and its reserved space too: the intent is that no portrait
is coming, so nothing should be held open for one.

Then find every place a photo or its slot appears and remove it properly —
a deleted `<img>` alone leaves orphaned assets and broken metadata. Cover
whichever of these exist:

1. **Rendered instances and reserved slots** — hero, about page, footer,
   any bio block or author card. Remove the element, its aspect box, and
   any wrapper that exists only to hold it. A slot left holding empty space
   is the same problem in a different form.
2. **The asset files** — delete the source image and any generated
   variants, srcset entries, or preload hints pointing at them.
3. **Layout that assumed an image** — grid columns, flex rows, or fixed
   heights sized around the photo need rebalancing so the text doesn't sit
   in a hole. Do not leave an empty column.
4. **Structured data** — remove `image` from any JSON-LD `Person` block.
5. **Social preview metadata** — `og:image` and `twitter:image`. If either
   currently points at the profile photo, **replace rather than delete**:
   an empty og:image makes every shared link render as a blank card. Use an
   existing non-photo site image, or a simple wordmark/typographic card
   consistent with the site's design. Note in the PR which you chose.
6. **Alt text and captions** referencing the photo, and any CSS rules left
   with no element to style.

Keep the LinkedIn link wherever it already appears — that stays the place
the face lives.

## Definition of done

A branch dispatch/2026-08-31-tomgreenai-photo-01 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request. The PR description
lists every file touched, names which social-preview image was chosen and
why, and confirms no orphaned image assets or dangling CSS remain. Build
and lint pass. Branch from the default branch; independent of the other
open tomgreen.ai contracts. No push to the default branch.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-08-31.
