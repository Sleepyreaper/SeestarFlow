# Processing recipes and decision gates

These are starting profiles for S50 Pro data. They are not promises that a
slider value is correct for every target. Signal, integration, seeing, focus,
sampling, and field density decide how much processing an image can tolerate.

## The production branch we own now

```text
individual FITS
  -> SeestarFlow ingest / hash / QA
  -> Siril registration + integration
  -> GraXpert background extraction OR GradientXTerminator
  -> RC Astro NoiseXTerminator (one denoise stage)
  -> optional RC Astro StarXTerminator
  -> Siril independent stretches and color preparation
  -> Photoshop layered recombination and local finish
  -> optional masked StarShrink
  -> Lightroom catalog, keywords, output variants, and print soft proof
```

PixInsight is optional, not a missing dependency. It becomes useful later for
LocalNormalization, complex mosaics, advanced narrowband channel work, and
repeatable process containers. It does not need to be installed for this
production branch.

The owned RC Astro bundle contains GradientXTerminator, NoiseXTerminator,
StarXTerminator, and StarShrink. BlurXTerminator is not assumed.

## Target-class defaults

| Target class | Filter | Gradient owner | NXT | SXT | StarShrink | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Emission nebula | Dual-band in bright sky; either at dark site | GraXpert subtraction by default | Moderate, once | Usually | Sometimes | Stretch starless first; return stars around 55–75% visual strength |
| Galaxy | Broadband | GraXpert or selected GXT pass | Mild/moderate, once | Sometimes | Sometimes | Protect core, H-II knots, and tiny background galaxies |
| Open/globular cluster | Broadband | Mild GraXpert or GXT | Mild, once | Rarely | No | The stars are the subject; keep natural color and profiles |
| Reflection/dark nebula | Broadband, dark site | Very cautious or skip | Mild/moderate, once | Sometimes | Rarely | A background model can remove real faint dust |
| Wide Milky Way | Broadband, dark site | Only with a credible model | Mild, once | No | No | Retain the natural star field and large-scale structure |

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

## Gate 2: NoiseXTerminator

One denoise stage only. Noise should become quieter while still looking random.
Back off if the background becomes plastic, mottled, or visibly tiled. Do not
judge a linear result only through an aggressive screen stretch.

## Gate 3: StarXTerminator

SXT is optional. Keep both the stars-intact and separated paths. Reject the
separated version if bright stars leave dark holes, color rings, or smeared
nebula residue. Dense clusters usually look better without separation. When
separating linear data, leave Unscreen off and retain the original.

## Gate 4: GradientXTerminator and StarShrink

GradientXTerminator is the Photoshop alternative when GraXpert's model is not
credible, or a conservative residual pass after the remaining gradient is
proved. Protect the object and begin coarse/low-to-medium. StarShrink belongs
near the end, after recombination, only when stars overwhelm a non-stellar
subject. Mask feature stars and skip it for clusters.

## Photoshop master layers

Use this minimum top-to-bottom layer structure:

```text
OUTPUT CHECKS             (soft proof / gamut warning; normally hidden)
SIGNATURE OR WATERMARK    (proof export only)
FINAL COLOR               (adjustment layers; masked)
LOCAL CONTRAST            (masked luminosity, restrained opacity)
STAR CONTROL              (optional masked StarShrink)
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
