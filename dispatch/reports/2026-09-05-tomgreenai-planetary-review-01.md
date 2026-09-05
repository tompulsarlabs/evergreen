# Report — 2026-09-05-tomgreenai-planetary-review-01

Produced by the frontier/openai lane, 14.5 wall-minutes.

# PR #16 adversarial review

Reviewed supplied PR head `8db38c7fe7247aab827e43781f1d49dda0d24264` against `1e92fcb5992e678542c6e5c26bcd64cd920562a0`. Manual static review; no `code-review` skill was installed. The checkout remained unchanged. Tests were not executed under the read-only constraint; `git diff --check` was clean.

## Findings

### P1 — Retained decoders remain paused during subsequent captures

**Location:** `src/lib/capture-decoders.ts:76`

`rewindGoldenAssets()` pauses and rewinds the session’s retained videos (`src/lib/golden-path-assets.ts:188`), but `GoldenPathLayer` resets `plateSeeded` and `paperSeeded` only when the video object changes (`src/components/golden-path-layer.tsx:288`). During a parent-to-leaf capture in one open portal, those objects do not change. The follower therefore enters the seeded “follow” branch, which adjusts `playbackRate` but never calls `play()`. The decoder stays frozen at frame zero until its error exceeds 0.5 seconds, at which point it finally reseeks and resumes. Consequently, the second capture omits roughly the first half-second of both baked streams, including much of the hero breakout.

The existing “second run” E2E closes and reopens the portal, producing new video identities, so it cannot detect this same-session failure.

**Proposed fix:** Reset both seeded flags for every newly armed capture, or make the non-held follow branch resume a paused follower. Add a unit case with `seeded: true`, `paused: true`, and zero error, plus an E2E that performs parent capture followed by leaf capture without closing the portal and asserts decoder time advances immediately.

### P1 — Page takeover assumes navigation commits before the authored clock expires

**Location:** `src/components/orbit-portal.tsx:391`

The code calls `markGoldenPushed()` before `router.push()`, then unconditionally finishes and closes at `STILL_AT` (`src/components/orbit-portal.tsx:403`). It never observes whether the destination pathname actually committed. Prefetching at `src/components/operating-orbit-3d.tsx:432` improves the common case but does not guarantee success on a cold, slow, or failed request. If navigation takes longer than the remaining paper interval, the portal exposes the source page and the destination arrives later as a cut; if navigation fails, the capture resolves onto the wrong page.

**Proposed fix:** Add a destination-readiness handshake, such as observing the expected pathname/client marker, and retain the opaque takeover until that signal arrives. On a bounded failure timeout, restore the source state instead of marking the route landed. Add E2E coverage with the destination request delayed past `STILL_AT` and with the request aborted.

### P1 — Close-time history unwinding can skip the real destination page

**Location:** `src/components/orbit-portal.tsx:294`

Normal restoration validates both the runtime record and its pathname (`src/components/orbit-portal.tsx:309`), but the `unwinding` branch treats any numeric `portalStep` as an owned entry. The implementation already acknowledges that Next navigation can copy a portal step onto a non-map destination (`src/components/orbit-portal.tsx:166`).

A reproducible sequence is: capture into a case study, reopen the planetary portal on that page, then press Close. The first Back reaches the case-study entry carrying the stale earlier `portalStep`; unwinding sees only the number and continues backing through the old section and map entries, navigating away from the case study.

**Proposed fix:** Continue unwinding only when the step resolves to a live record whose pathname matches `window.location.pathname`, preferably also carrying a chain/session identifier. Otherwise stop unwinding on that entry. Add an E2E for capture → destination → reopen portal → Close, asserting the destination remains visible and the following Back restores the captured section.

### P2 — Conducted burst channels do not share the advertised shot clock

**Location:** `src/components/operating-orbit-3d.tsx:1399`  
**Location:** `src/app/globals.css:1145`

`OrbitFlare` and `OrbitNebula` correctly use `goldenBurstTime()` for conducted captures, but the membrane always derives its crest, light, throat, and colour from wall time. The DOM breakout is also a fixed 700 ms CSS animation. These channels therefore continue while a review clock is held and run at different relative speeds during compact captures, contradicting the “one event, one clock” guarantee in `src/lib/capture-timing.ts:40`.

**Proposed fix:** Use `flare.conducted ? goldenBurstTime() : wallTime` for every membrane calculation. Replace the conducted CSS animation with a shot-clock-driven effect, or explicitly pause/seek a Web Animations instance from the shot clock. Add integration assertions that holding or compacting the clock produces the same normalized flare, membrane, and breakout states.

### P2 — Invisible and still-arriving bodies remain keyboard controls

**Location:** `src/components/operating-orbit.tsx:267`  
**Location:** `src/components/operating-orbit-3d.tsx:642`

The live labels are unconditional anchors and are never removed from the tab order. Keyboard activation calls `startCapture()` directly, which has no arrival/settled guard. Focusing an otherwise invisible anchor also forces it fully opaque through `src/app/globals.css:794`.

Pointer gating is incomplete as well: `landed > 0` marks a body settled at `src/components/operating-orbit-3d.tsx:1713`, even though its arrival curve continues until `arrived === 1`. Direct nameplate hit-testing at `src/components/operating-orbit-3d.tsx:824` bypasses the `spot.settled` check used for body hits. Thus bodies can be activated during the final quarter of their flight, and keyboard users can activate them from the beginning.

**Proposed fix:** Publish a single per-body readiness predicate, enforce it in `startCapture()` as defense in depth, use it for both label and body hit-testing, and set `tabIndex={-1}`/appropriate disabled semantics until ready. Add pointer, Enter, and Space tests during initial arrival and after full settlement.

### P2 — The advertised hidden-tab recovery path is not wired

**Location:** `src/lib/golden-path-store.ts:366`  
**Location:** `src/components/orbit-portal.tsx:334`

The store accepts a `"hidden"` abort reason and the integration report claims hidden tabs settle synchronously, but no planetary production code calls `abortGoldenPath("hidden")`. The only caller is a unit test. The portal relies on rAF plus a timeout; rAF stops in a hidden tab and background timers may be throttled, so this is neither synchronous nor the described recovery behavior.

**Proposed fix:** Install a portal-level `visibilitychange` listener that settles a confirmed destination or aborts a pre-navigation capture immediately when `document.hidden` becomes true, including local flare cleanup. Add an integration test dispatching `visibilitychange` before and after route commitment.

### P2 — Popstate and watchdog termination can leave a permanent conducted remnant

**Location:** `src/components/orbit-portal.tsx:304`  
**Location:** `src/lib/golden-path-store.ts:333`

Escape explicitly clears `flare`, but the pre-push popstate abort does not. Conducted flares intentionally have no wall-clock cleanup timer (`src/components/orbit-portal.tsx:589`). Once aborted, `goldenShotTime()` returns `SHOT_END`; `OrbitNebula` then samples a still-live burst time and continues rendering the same nonzero afterglow indefinitely (`src/components/orbit-nebula.tsx:271`). A watchdog completion before route push has the same ownership gap because the store cannot clear the portal’s local flare state.

**Proposed fix:** Centralize terminal visual cleanup in a subscription/effect that clears every conducted flare whenever the shot reaches `done` or `aborted`, rather than duplicating cleanup only on selected exits. Add Back-during-breakout and watchdog-expiry tests that assert the remnant disappears and the restored map is idle.

### P3 — Runtime history records grow without pruning

**Location:** `src/components/orbit-portal.tsx:147`

Every descent/open inserts another record at `src/components/orbit-portal.tsx:171`, but no code deletes or clears records. Entries made unreachable when a new push truncates browser forward history, and entries intentionally popped during dismissal, remain retained for the lifetime of the root portal component. The repeated-descent E2E checks canvas and DOM counts but not this JavaScript registry.

**Proposed fix:** Model the active history chain explicitly and prune records when forward history is replaced or a dismissed chain is fully unwound. Add a history-model test that repeatedly descends, backs, and branches while asserting the registry remains bounded by reachable portal entries.

### P3 — The checked-in behavior report describes obsolete timings

**Location:** `review-vfx/golden-path-integration/INTEGRATION-REPORT.md:41`

The report claims 5.23 s full and 3.35 s compact captures, with a 0.75/0.45 s approach in its table (`review-vfx/golden-path-integration/INTEGRATION-REPORT.md:223`). The implementation and timing tests define 5.32 s, 3.41 s, and 0.84/0.50 s respectively (`src/lib/capture-timing.ts:26`). `src/components/orbit-portal.tsx:218` also retains the old 5.23 s figure.

**Proposed fix:** Update the report and comments to the current timing table, ideally generating the published table from the canonical constants so future timing changes cannot silently invalidate the review artifact.

## Confirmed sound sections

- The resolution policy is genuinely data-driven: `src/lib/planet-model.ts:219` maps parents to child-system release, internal leaves to paper takeover, and external routes to immediate departure without hard-coded capture IDs.
- External navigation remains inside the original user activation at `src/components/orbit-portal.tsx:553`; it is not delayed behind the cinematic.
- The pure release curves in `src/lib/capture-release.ts:77` and the piecewise full/compact mapping in `src/lib/capture-timing.ts:68` are internally continuous and well covered by their unit tests. The clock-consumer defects above occur outside those pure models.
