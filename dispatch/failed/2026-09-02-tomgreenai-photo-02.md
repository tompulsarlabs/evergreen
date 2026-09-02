---
id: 2026-09-02-tomgreenai-photo-02
type: build
state: failed
repo: tompulsarlabs/tomgreen.ai
lane: workhorse
pool: anthropic
created: 2026-09-02T18:30:00+02:00
created_by: tom
expires: 2026-09-04T18:30:00+02:00
budget: { wall_minutes: 25 }
---

## Task

Re-queue of `2026-08-31-tomgreenai-photo-01`, which the runner refused on
2026-09-01 at the attribution gate because of a runner bug (equality against
one address; fixed 2026-09-02), not on merit.

Remove Tom's profile photo from the site. His face belongs on LinkedIn; the
site should carry proof of work instead.

**Start by establishing what actually exists on the current `main`.** PR
#10 (merged 2026-09-01, "One object, two layers") described PersonalHero as
carrying "a portrait slot that holds its own aspect box so adding the
photograph later shifts nothing", and PR #12 recomposed Home on 09-02 — so
the site may hold a reserved *empty slot*, a rendered photo, or neither.
Remove the slot and its reserved space too: no portrait is coming, so
nothing should be held open for one. If neither a photo nor a slot exists
any more, open no PR: say so in the summary between the report markers,
naming the components checked, and stop.

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

A branch dispatch/2026-09-02-tomgreenai-photo-02 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request. The PR description
lists every file touched, names which social-preview image was chosen and
why, and confirms no orphaned image assets or dangling CSS remain. Build
and lint pass. Branch from the default branch; independent of the other
open tomgreen.ai contracts. No push to the default branch. Or, if no photo
and no slot exist, no PR and a summary that says so.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-09-02 — or the
contract's report states that no photo or slot remains, naming the
components checked.

outcome:
  claimed_at: 2026-09-02T19:06:50+02:00
  exit: attribution
  note: next commit would author 'tompulsarlabs <tom@pulsarlabsai.com>' — not the connected address
