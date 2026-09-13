# S50 Pro early-image benchmarks — September 2026

These are independently posted early results, not ZWO advertising images. They are useful as a reality check for our first nights, but not a promise: sky quality, target altitude, transparency, framing, and processing differ.

## What the first images say

| Target / source | Acquisition reported | What it tells us | Our first-run standard |
| --- | --- | --- | --- |
| M31, Henry W. Coe State Park, Reddit | 200 x 30 seconds in Alt-Az; 100 minutes; straight from the S50 Pro app | Even without an EQ head or external processing, a short supervised session can make a shareable Andromeda image. Satellite streaks and app processing remain visible realities. | A 45–60 minute Marietta M31 session should give a recognizable core and dust lane if the east/northeast window is genuinely clear. It is a systems test, not a comparison to a dark-site result. |
| M33, Astronomie Pratique test | 30-second sub-exposures; 3 hours in one night; app result then a conventional astro-processing pass | M33 is feasible but rewards time. The conventional workflow recovered additional color and detail. | Do not judge the scope by a 10-minute M33 attempt. Target 3+ hours across supervised sessions; use our free and paid pipelines only after saving FITS. |
| M31, Astronomie Pratique test | Several 2–3 hour nights, combined and manually processed | Multi-night integration is normal and makes M31 a serious project rather than an overnight gamble. | Preserve framing, filter, exposure family, and session notes so we can combine later nights. |
| M33, ScopeTrader user example | 311 x 60 seconds; internally processed | The Pro can produce impressive deep integrations, but this is an early community example and no sky/site conditions are documented. | Treat 5+ hour results as a later EQ benchmark, not the minimum needed to impress friends. |

## The one setting we cannot miss

The early S50 Pro field test found that **individual FITS saving is enabled during an active live-stack session**, via the three-dot menu and the option described as “save every frame.” It is not a permanent global app preference in that test. Before every serious run:

1. Start the target and confirm focus/stacking.
2. Open the live-view three-dot menu.
3. Turn on **Save every frame** (wording may differ slightly in our app version).
4. After a few accepted frames, verify the session shows individual FITS files before committing an hour.

The Seestar app stack is our live-show result. The individual FITS files are the material for Siril, GraXpert, RC Astro, and Photoshop.

## Monday: what “good” actually means

Success is not a wall print on night one. We win if we bring home:

- a clean 10–15 minute live-stack image to show people;
- individual FITS files from both a broadband target and a dual-band target;
- the device-generated stack for comparison;
- a session log with actual accepted integration, filter, exposure, position, and visible obstructions;
- one 30–60 minute M31 or North America Nebula data set that processes cleanly in the free pipeline.

If the app stack is attractive in 10–15 minutes but the FITS data is preserved, the session has already succeeded. The final share/print version comes from stacking more of those authentic short exposures over later supervised sessions.

## Preparation checklist while Adobe and RC Astro install

- Install/update the Seestar app to the current production version and sign in.
- In RC Astro, confirm **NoiseXTerminator**, **BlurXTerminator**, and **StarXTerminator** open normally; do not run them on Monday’s raw FITS individually.
- In Photoshop, create two export presets: `social-watermarked` and `print-unwatermarked`.
- In Lightroom Classic, create an import preset with copyright metadata, creator name, contact/website, and a `Seestar S50 Pro` keyword.
- Keep original FITS and 16-bit TIFF masters separate from all JPEG exports.
- On the first real run, do not use generative fill, AI sky replacement, or fabricated structure in any image described as astrophotography. RC Astro’s denoise/deconvolution/star processing is a finishing tool; the captured photon data remains the source.

## Sources

- [M31: 100 minutes / 200 x 30 seconds, straight from the app](https://www.reddit.com/r/seestar/comments/1w9thw6/m31_andromeda_galaxy_from_s50_pro/)
- [Independent S50 Pro test: Milky Way, M33, M31 and processing comparison](https://www.astronomie-pratique.com/test-seestar-s50-pro/)
- [Early M33 311 x 60-second community example](https://scopetrader.com/forum/seestar-s50-pro-example-astrophotos/smart-telescopes/0km1557j7126us7n8yb4wv1ge7rmphf669un316s/)
- [Early S50 Pro FITS-saving observation](https://www.blickohnegrenzen.de/2026/09/03/seestar-s50-pro-test-tag-7-8-wolkenfrust-fits-rohdaten/)
