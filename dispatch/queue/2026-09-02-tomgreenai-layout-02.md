---
id: 2026-09-02-tomgreenai-layout-02
type: build
state: open
repo: tompulsarlabs/tomgreen.ai
lane: frontier
pool: anthropic
created: 2026-09-02T18:30:00+02:00
created_by: tom
expires: 2026-09-04T18:30:00+02:00
budget: { wall_minutes: 45 }
---

## Task

Re-queue of `2026-08-28-tomgreenai-layout-01`, which the runner refused on
2026-09-01 at the attribution gate because of a runner bug (equality against
one address; fixed 2026-09-02), not on merit.

**Establish current state first.** PR #12 ("One alignment rule, a
recomposed Home, and a planetary map that works", merged 2026-09-02) may
already have introduced the shared container primitive this contract asks
for. Read the current layout system on `main` before changing anything, then
verify at the widths in step 6. Fix only what still fails. If nothing fails,
open no PR: say so in the summary between the report markers, listing the
widths checked, and stop.

The 08-28 observation, on a 28" external monitor (~2000px viewport, /about
"through-line" page): three different alignment references coexisted on one
page — the header logo's left edge (~587px), the content column's left edge
(~513px), and the scroll indicator centered on the true viewport center
(~1000px) — with the year rail pinned to the raw right edge. The composition
was visibly tuned to one development viewport. Section content also sat
half-faded at rest, suggesting scroll-driven opacity keyed to absolute pixel
offsets.

Fix the layout system, not the symptoms:

1. **One shared container primitive** (max-width + margin-inline auto +
   fluid padding-inline via clamp()) used by the header, every section, and
   the footer — alignment becomes true by construction on any width.
2. **Decorative layers** (the radial-line canvas, backgrounds) may be
   full-bleed but must center on the container's content box, never define
   alignment themselves.
3. **No pixel offsets tuned to a viewport.** Fluid type and spacing in
   rem/clamp(). The year rail becomes a reserved grid column (or hides
   below a breakpoint) instead of a fixed-right overlay that can collide
   with content.
4. **Viewport units:** dvh/svh instead of vh for full-height sections
   (mobile URL-bar resize breaks vh).
5. **Scroll-driven animation keyed to element-relative progress**
   (IntersectionObserver or scroll-timeline percentages), never absolute
   pixel scroll positions.
6. Verify at 375, 768, 1440, 2560, and 3440 CSS px widths and at 1x and 2x
   DPR; every page, both themes if applicable.

## Definition of done

A branch dispatch/2026-09-02-tomgreenai-layout-02 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request containing whatever of
the five fixes still applied, with a PR description listing the widths
verified. Branch from the default branch; independent of the other open
tomgreen.ai contracts. No push to the default branch. Or, if nothing
failed, no PR and a summary that says so with the widths checked.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-09-02 — or the
contract's report states that every listed width passed on the current
`main`.
