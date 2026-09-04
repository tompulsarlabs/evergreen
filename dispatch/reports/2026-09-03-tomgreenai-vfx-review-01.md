# Report — 2026-09-03-tomgreenai-vfx-review-01

Produced by the frontier/openai lane, 5.7 wall-minutes.

# PR #13 review — Golden-path VFX asset proof

Reviewed head `aa180e8db3e71a26826a663027098e269de71994` against `main` at `1e92fcb5992e678542c6e5c26bcd64cd920562a0`.

## Verdict

The title is narrowly accurate: the diff changes no site route, component, public asset, package/build script, Next.js configuration, or CI workflow. The additions are confined to `.gitignore`, `review-vfx/golden-path-asset-proof/`, and `tools/blender/golden-path-proof/`, with no references from the application.

It is not an inert PR, however. It adds 91 files, roughly 5,000 lines of asset-generation code, and 40.4 MB of review artifacts. The review/build path has correctness and reproducibility defects requiring normal PR scrutiny.

## Findings

### [High] Partial frame sets are silently published as complete videos

`tools/blender/golden-path-proof/render_review.py:770` collects only frames that happen to exist, and lines 773–790 deliberately encode shortened or gapped ranges instead of failing. Delivery then runs automatically at `tools/blender/golden-path-proof/render_review.py:987`, even when `--frames` or `--list` requested only a preview.

Consequently, the documented quick-look command at `tools/blender/golden-path-proof/README.md:56` can overwrite the named review deliverables with one-frame videos. An interrupted render or stale cache can similarly produce a shortened “full” master without any build failure. This defeats the motion gate’s exact-frame guarantee.

Proposed fix: require `nums == list(range(f_start, f_end + 1))` before encoding, report every missing frame, and permit delivery only for a complete render or an explicit delivery command. Post-encode verification should also assert frame count and duration before replacing an existing artifact.

### [High] The current GLB exceeds the documented integration budget by almost 10× while the main report says it passes

`review-vfx/golden-path-asset-proof/asset-report.md:256` reports `fragments.glb` as 364.1 KB, and line 281 says it is below the 1.6 MB budget without textures. The committed GLB is actually 15,649,764 bytes and contains 36 embedded PNG images. `review-vfx/golden-path-asset-proof/CHANGES-v2.md:75` acknowledges the 15.4 MB textured asset, while `review-vfx/golden-path-asset-proof/asset-report.md:333` and `tools/blender/golden-path-proof/README.md:109` still claim no textures are baked.

A gate reviewer could therefore approve an asset based on a stale, materially false integration-readiness statement.

Proposed fix: regenerate the authoritative report from the current artifact and either mark the GLB review-only/noncompliant or reduce it to the stated budget using shared atlases, lower resolutions, appropriate texture compression, and geometry compression. Remove all contradictory “no textures” claims.

### [Medium] Cached renders are reused across incompatible settings

`tools/blender/golden-path-proof/render_review.py:368` treats an existing `Image_<frame>.exr` as complete without recording or comparing scale, crop, samples, tuning values, bounces, step rate, Blender version, or source revision.

This directly conflicts with `tools/blender/golden-path-proof/README.md:59`, whose border/tuning example writes into the same default `render_v2` cache later used by the final `--stills` render. The final command can silently reuse a cropped, low-quality, or tuned look-development plate and publish it as an approval still.

Proposed fix: key caches by a manifest/hash of every output-affecting setting and source revision, rejecting mismatches. At minimum, give look-development commands a distinct cache tag and require `--force` before replacing final-cache entries.

### [Medium] The advertised clean regeneration path does not reproduce the current review package or its validation evidence

`tools/blender/golden-path-proof/regenerate.sh:8` invokes the default renderer only. It does not select the committed V3 motion mode, create the V1/V2 comparisons, regenerate either report, or run the fitting/validation tooling, despite `tools/blender/golden-path-proof/README.md:40` saying it produces “everything above.”

Moreover, `tools/blender/golden-path-proof/motion_report.py:91` merely appends an optional ignored cache note; it does not calculate the hash, PSNR, temporal-residual, glyph-pixel, or luminance checks asserted at `review-vfx/golden-path-asset-proof/motion-report-v3.md:41`. The source PNG sequence called “the archival source” at line 101 is also absent from the PR. A clean reviewer can regenerate for roughly ten CPU-hours, but cannot reproduce the stated validation report through the documented command.

Proposed fix: provide explicit versioned regeneration targets. The V3 target should run `render_review.py --seq3`, execute a committed validator that calculates the reported metrics, regenerate `motion-report-v3.md`, and fail if artifact hashes, frame counts, or thresholds differ. Document separate commands for the legacy, V2-still, and V3-motion packages.

## Verification notes

- All nine added Python files parse successfully as Python syntax.
- The committed V3 MP4 containers contain 145 frames over 4.833333 seconds and 290 frames over 9.666667 seconds respectively, with metadata before media data.
- The GLB has a valid glTF 2 header and contains 12 nodes, 12 meshes, 12 animations, 24 materials, and 36 embedded images.
- Full pipeline execution was not attempted because the checkout is read-only and does not contain the external Blender, NumPy, SciPy, OIDN, Pillow, or FFmpeg dependencies.
- No `code-review` skill was installed in this harness; the review was performed directly.
