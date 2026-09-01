---
id: 2026-08-28-tomgreenai-layout-01
type: build
state: failed
repo: tompulsarlabs/tomgreen.ai
lane: frontier
pool: anthropic
created: 2026-08-28T10:55:00+02:00
created_by: tom
expires: 2026-09-04T10:55:00+02:00
budget: { wall_minutes: 45 }
---

## Task

Make the site's layout genuinely display-independent. Observed on a 28"
external monitor (~2000px viewport, /about "through-line" page): three
different alignment references coexist on one page — the header logo's left
edge (~587px), the content column's left edge (~513px), and the scroll
indicator centered on the true viewport center (~1000px) — with the year
rail pinned to the raw right edge. The composition was visibly tuned to one
development viewport; on wider displays the elements drift apart. Also: the
section content sits half-faded at rest, suggesting scroll-driven opacity
keyed to absolute pixel offsets, which lands mid-transition on taller
viewports.

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

A branch dispatch/2026-08-28-tomgreenai-layout-01 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request, containing the shared
container refactor and the five fixes above, with a PR description listing
the widths verified. No push to the default branch.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-08-28.

outcome:
  claimed_at: 2026-09-01T17:01:18+02:00
  exit: attribution
  note: next commit would author 'tompulsarlabs <tom@pulsarlabsai.com>' — not the connected address
