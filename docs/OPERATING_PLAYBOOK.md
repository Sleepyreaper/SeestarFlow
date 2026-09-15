# SeestarFlow operating playbook

This is the canonical house workflow. It answers three questions at every
stage: what do we do, which tool owns the job, and what evidence must survive.
It is designed for authentic astrophotography made from our captured photons;
no generative fill, replacement sky, or invented astronomical structure is part
of the process.

## The short version

```text
plan -> capture individual FITS -> verified archive -> measure/reject ->
Siril register/integrate -> common 32-bit linear FITS ->
GraXpert OR GradientXTerminator for gradients ->
NoiseXTerminator once -> optional StarXTerminator -> stretch ->
Photoshop layered finish -> optional StarShrink ->
Lightroom catalog/proof/export -> release ledger -> next-night feedback
```

The word **OR** matters. More installed tools do not automatically make a
better image. Two aggressive gradient removals or two denoisers can erase real
faint signal.

## 1. Plan the photons

Choose one primary target from its physics and the available sky window:

| Object | Filter | First useful result | Portfolio goal |
| --- | --- | ---: | ---: |
| Emission nebula | LP/dual-band in suburban sky | 15–30 min | 90–180+ min |
| Galaxy | LP off / broadband | 20–40 min | 120–300+ min |
| Open cluster | LP off / broadband | 10–20 min | 30–60 min |
| Reflection or dark nebula | LP off, dark site strongly preferred | 30–60 min | 180+ min |

Integration may be combined across nights when target, camera mode, filter, and
framing are compatible. Keep nights as separate sessions until registration;
this preserves provenance and makes it possible to reject one weak night.

### Exposure and mount decision

- Stock Alt-Az: use 10 seconds as the dependable baseline. Test 30 seconds only
  against the same target and conditions.
- TH10 EQ: polar-align within 1 degree, then compare 10, 30, and 60 seconds.
- Select the duration that produces the most **accepted integration per clock
  hour**, not the duration with the largest number printed in the app.
- EQ can win even at 10 seconds through lower field rotation, steadier coverage,
  and less edge cropping. Sixty seconds is a capability to test, not a goal.

Use [EQ_EXPOSURE_TEST.md](EQ_EXPOSURE_TEST.md) for a controlled comparison.

## 2. Configure and capture

Use [APP_FIELD_CARD.md](APP_FIELD_CARD.md) at the telescope. The production
defaults are RAW live view, Save Each Frame on, autofocus on, trail rejection
on, dark correction on, and 10-second Alt-Az exposures. Auto LP stays off so
filter choice is deliberate.

Before a long block:

1. Place the tripod on stable ground; do not use a vehicle roof.
2. Shield direct lamps without enclosing the telescope or blocking ventilation.
3. Level in Alt-Az or polar-align in EQ; complete horizontal calibration.
4. GOTO, plate solve, autofocus, and inspect a two-minute test.
5. Confirm a target `_sub` folder is receiving individual FITS files.
6. Record target, UTC/local time, mode, sub length, filter, weather, interruptions,
   and accepted-integration goal.
7. Stop for rain, unsafe wind, instability, or condensation on electronics.

The app stack is the outreach preview. The individual FITS files are the
production negative.

## 3. Ingest without losing ownership

Stop enhancement, stow, power down, and connect the Seestar by USB-C. Copy the
complete target folder, including `_sub`; never process directly on the device.

```powershell
python -m seestarflow ingest `
  --source "E:/Seestar/MyWorks/M27" `
  --target M27 `
  --site home `
  --filter dualband `
  --mount altaz
```

Ingest copies and hashes every original, writes `manifest.json`, and records the
session in the local catalog. Before erasing the telescope, verify counts,
open several archived FITS files, and make a second backup. Originals remain
immutable; corrections always create new products.

## 4. Measure, register, and integrate in Siril

```powershell
python -m seestarflow analyze --session ".\library\M27\<session>"
python -m seestarflow stack --session ".\library\M27\<session>"
```

Review the generated `quality.csv` and rejected frames. Automatic thresholds
are triage, not permission to delete. Siril registers the approved subs,
rejects outliers during integration, and preserves `stack_linear.fit` as the
common 32-bit linear master.

For comparisons, freeze this master and its SHA-256. Free and paid branches
must start from the same bytes.

## 5. Correct the background: choose one owner

### Default: GraXpert while linear

Run subtraction and save its background model:

```powershell
python -m seestarflow linear --stack "D:/Astro/.../stack_linear.fit"
```

The model should show broad illumination, not the galaxy halo, nebula, or dark
dust. If it contains the subject, reduce flexibility, crop unstable borders,
or skip the correction.

### Alternative: GradientXTerminator in Photoshop

Use GradientXTerminator when an image is already in Photoshop or GraXpert's
model fails. Select background areas while protecting the object; begin with a
coarse/low-to-medium pass. A second small residual correction is allowed only
when the first model is saved and the remaining gradient is obvious. Do not run
two full-strength background removals by habit.

## 6. Use the RC-Astro tools we own

The owned Photoshop bundle is **GradientXTerminator, NoiseXTerminator,
StarXTerminator, and StarShrink**. NoiseXTerminator and StarXTerminator licenses
also work in the stand-alone CLI. BlurXTerminator is a separate license and is
not part of this workflow.

### NoiseXTerminator — once

Use one moderate pass, preferably while data are still linear or on the linear
starless branch. If GraXpert denoise was used for the free branch, do not add
NoiseXTerminator. Reject a result that looks waxy, tiled, or removes fine random
texture along with the noise.

### StarXTerminator — only when separation helps

- Emission nebula: usually useful; separate early and stretch object and stars
  independently.
- Galaxy: optional; inspect the core, H-II knots, and small background galaxies.
- Open/globular cluster: normally skip because the stars are the subject.
- Linear data: keep Unscreen off and preserve both starless and stars-intact
  references.

The `premium` command creates a conservative NXT/SXT CLI recipe. Use
`--star-separate` only after the target-class decision:

```powershell
python -m seestarflow premium `
  --linear "D:/Astro/.../linear/gradient_corrected.fits" `
  --kind nebula `
  --star-separate
```

### StarShrink — late, masked, optional

Use StarShrink after stars are recombined when they overwhelm a nebula or
galaxy. Start subtle and mask bright feature stars. Skip it for clusters, and
never use it to disguise poor focus, tracking, or saturated stars. StarShrink
changes star presentation; it is not deconvolution.

## 7. Stretch and finish without destroying the master

Stretch in Siril or with controlled Photoshop curves without clipping the black
point or target core. Export 16-bit TIFFs for the object, stars, and a
stars-intact reference. Keep the 32-bit linear FITS untouched.

In Photoshop use a layered master:

```text
OUTPUT CHECKS             soft proof / gamut warning; hidden normally
SIGNATURE OR WATERMARK    public proof only
FINAL COLOR               adjustment layers; masked
LOCAL CONTRAST            restrained and masked
STAR CONTROL              optional StarShrink result or star-opacity control
STARS                     Screen recombination when separated
STARLESS OBJECT           independently stretched subject
BACKGROUND CONTROL        curves/color; black point never clipped
REFERENCE                 stars-intact source, hidden but retained
```

Use `scripts/SeestarFlow_LayeredFinish.jsx` to build the scaffold. Keep two
finishes when useful: a restrained natural edition and a clearly labeled
cinematic color edition. Both must use the same captured structure.

## 8. Lightroom is the library and output room

Lightroom does not stack FITS and should not contain thousands of subs. Import
the layered-master export and release variants. Add target/catalog name,
location at a privacy-safe level, telescope, filter, mount, sub length, accepted
integration, capture dates, creator, copyright, and processing version.

Use Lightroom for final global color consistency, crop variants, output
sharpening, watermark presets, print soft proof, and collections. Do not add a
second AI-denoise pass.

## 9. Release and preserve

Export at least:

- archive: full-resolution 16-bit TIFF, no watermark;
- portfolio: full-resolution color-managed JPEG;
- proof/social: resized JPEG with a subtle watermark;
- print: lab-profiled TIFF or JPEG as requested by the lab.

```powershell
python -m seestarflow release `
  --file "D:/Astro/M27-portfolio-v01.jpg" `
  --target M27 `
  --variant portfolio
```

The release ledger hashes the exact published file. Preserve originals,
manifest, session notes, quality report, common linear master, layered PSD,
recipe, and exports. A watermark is advertising; the raw archive, metadata,
hashes, and backups are the ownership evidence.

## 10. Close the feedback loop

After every session record:

- accepted/attempted frames and accepted integration per clock hour;
- median FWHM, ellipticity, background, and saturation;
- focus changes, wind, dew, direct-light problems, and interruptions;
- whether filter and sub length helped this object;
- which processing stage failed first at 100% inspection.

Change one acquisition variable on the next comparable night. If processing
cannot reveal clean structure without artifacts, the answer is normally more
accepted integration, better focus/stability, a darker site, or the correct
filter—not a stronger slider.

## Current software boundary

- Required/free: SeestarFlow, Siril, GraXpert.
- Owned production: RC-Astro Photoshop bundle, Photoshop, Lightroom.
- Optional later: PixInsight for LocalNormalization, mosaics, advanced channel
  combination, and repeatable process containers.
- Not assumed: BlurXTerminator or any generative imaging service.

RC-Astro references: [Photoshop bundle](https://www.rc-astro.com/software/photoshop-bundle/),
[stand-alone tools](https://www.rc-astro.com/stand-alone-rc-astro-tools/),
[StarXTerminator usage notes](https://www.rc-astro.com/starxterminator-usage-notes/),
and [NoiseXTerminator manual](https://www.rc-astro.com/noisexterminator-2-ai3-user-manual-pixinsight/).
