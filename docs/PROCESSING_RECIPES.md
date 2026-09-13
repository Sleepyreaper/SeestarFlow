# Processing recipes and decision gates

These are starting profiles for S50 Pro data. They are not promises that a
slider value is correct for every target. Signal, integration, seeing, focus,
sampling, and field density decide how much processing an image can tolerate.

## The production branch we own now

```text
individual FITS
  -> SeestarFlow ingest / hash / QA
  -> Siril registration + integration
  -> GraXpert background extraction only
  -> RC Astro BlurXTerminator
  -> RC Astro NoiseXTerminator (one denoise stage)
  -> optional RC Astro StarXTerminator
  -> Siril independent stretches and color preparation
  -> Photoshop layered recombination and local finish
  -> Lightroom catalog, keywords, output variants, and print soft proof
```

PixInsight is optional, not a missing dependency. It becomes useful later for
LocalNormalization, complex mosaics, advanced narrowband channel work, and
repeatable process containers. It does not need to be installed for this
production branch.

## Linear defaults

| Target class | Filter | GraXpert | BXT stars / nonstellar | NXT | SXT | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Emission nebula | Dual-band in bright sky; either at dark site | Subtraction, smoothing 0.20 | 0.20 / 0.32 | 0.50, one pass | Usually | Stretch starless first; return stars around 55–75% visual strength |
| Galaxy | Broadband | Subtraction, smoothing 0.15–0.20 | 0.20 / 0.35 | 0.45, one pass | Sometimes | Protect core and star-forming knots; avoid waxy dust lanes |
| Open/globular cluster | Broadband | Subtraction, smoothing 0.15–0.20 | 0.12 / 0.18 | 0.35, one pass | Rarely | The stars are the subject; do not force a starless workflow |
| Reflection/dark nebula | Broadband, dark site | Very cautious subtraction | 0.18 / 0.28 | 0.40–0.45 | Sometimes | A background model can accidentally remove real faint dust |
| Wide Milky Way | Broadband, dark site | Only if model is clearly credible | Off or extremely mild | 0.30–0.40 | No | Correct distortion and reject aircraft/satellite trails; retain natural star field |

Run the defaults through SeestarFlow:

```powershell
# Paid production handoff: gradient correction only
python -m seestarflow linear --stack "D:/Astro/.../stack_linear.fit"

python -m seestarflow premium `
  --linear "D:/Astro/.../linear/gradient_corrected.fits" `
  --kind nebula `
  --star-separate

# Free comparison branch: GraXpert performs the single denoise stage
python -m seestarflow linear `
  --stack "D:/Astro/.../stack_linear.fit" `
  --grax-denoise
```

## Gate 1: background extraction

Always save the model with `-bg`. Inspect it stretched. It should contain broad
illumination gradients, not recognizable nebula arms, galaxy halos, IFN, or
dark-dust structure. If it contains the subject, reduce model flexibility,
change samples, crop unstable borders first, or skip extraction.

GraXpert documents its command-line background extraction and saved background
model in the [official project](https://github.com/Steffenhir/GraXpert/).

## Gate 2: BlurXTerminator

Judge at 100% and 50%, not fit-to-screen only. Compare:

- small and large stars in all four corners;
- a bright-star halo near the target;
- the faintest real filament or dust lane visible before correction;
- the galaxy/nebula core.

Back off if stars acquire black rims, tiny stars disappear, or the background
develops rope-like detail. The number is a ceiling, not a target.

## Gate 3: NoiseXTerminator

One denoise stage only. Noise should become quieter while still looking random.
Back off if the background becomes plastic, mottled, or visibly tiled. Do not
judge a linear result only through an aggressive screen stretch.

## Gate 4: star separation

SXT is optional. Keep both the stars-intact and separated paths. Reject the
separated version if bright stars leave dark holes, color rings, or smeared
nebula residue. Dense clusters usually look better without separation.

## Photoshop master layers

Use this minimum top-to-bottom layer structure:

```text
OUTPUT CHECKS             (soft proof / gamut warning; normally hidden)
SIGNATURE OR WATERMARK    (proof export only)
FINAL COLOR               (adjustment layers; masked)
LOCAL CONTRAST            (masked luminosity, restrained opacity)
STARS                     (Screen/Linear Dodge as tested; independent opacity)
STARLESS OBJECT           (main stretched object)
BACKGROUND CONTROL        (masked curves/color, never clipped)
REFERENCE                 (stars-intact stretch, hidden but retained)
```

Run `File > Scripts > Browse` in Photoshop and select
`scripts/SeestarFlow_LayeredFinish.jsx` to build this scaffold from the 16-bit
starless, stars, and optional stars-intact TIFFs. It sets the star layer to a
conservative 65% Screen starting point and saves a layered PSD; final opacity,
masks, and curves remain image-specific.

Do not use generative fill, replacement sky, painted nebulosity, or cloning that
creates new astronomical structure in a release labeled as an astrophotograph.
Dust spots, satellite trails, and obvious sensor artifacts may be removed when
the edit is disclosed in the recipe.

## Lightroom's job

Lightroom is the catalog and release manager, not the FITS processor:

- one catalog or collection per year;
- keywords for target, catalog number, site label, telescope, filter, mount,
  integration, and processing version;
- color labels for `candidate`, `keeper`, `print-approved`, and `released`;
- output presets for social proof, portfolio, and print-lab handoff;
- never import thousands of raw FITS subs into Lightroom.
