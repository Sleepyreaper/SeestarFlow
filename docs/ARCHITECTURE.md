# Architecture

SeestarFlow separates acquisition evidence from processing products. Every stage
has a narrow responsibility and leaves enough information to repeat or audit it.

## Data flow

```text
camera/removable source
  -> discovery
  -> verified immutable copy
  -> FITS metadata catalog + manifest
  -> per-frame measurement
  -> accepted list + rejection reasons
  -> disposable staging directory
  -> Siril registration/integration
  -> common linear master
       -> free branch
       -> production branch (RC Astro -> Siril -> Photoshop -> Lightroom)
```

## Archive layout

```text
library/
  catalog.db
  TARGET/
    YYYY-MM-DD_site_filter_mount/
      originals/             copied FITS; never processed in place
      manifest.json          source path, header, and SHA-256 for every frame
      quality.csv            measurements and rejection reasons
      approved.lst           exact frames admitted to integration
      products/
        YYYYMMDD_HHMMSS/
          lights/            hard-linked or copied disposable staging files
          process/           Siril sequences and registered data
          stack_linear.fit   common comparison boundary
          stack_report.json  registration yield and counts
          linear/            gradient/denoise products and recipe.json
          rcastro/           optional premium products and recipe.json
          photoshop/         layered PSD and release-ready TIFF/JPEG products
```

`config.toml`, `library/`, raw FITS files, and all generated media are ignored by
Git. The repository contains the method, not anybody's images.

## Ingest and provenance

`ingest` recursively discovers FITS files, ignores app stacks when `STACKCNT`
indicates multiple combined frames, computes SHA-256, copies each source into an
independent archive, verifies the copied hash, and records selected headers in
SQLite and JSON.

Copying is intentional. A hard link between a removable/source folder and the
archive would not be immutable because both names would refer to the same bytes.

## Quality gate

`analyze` measures a downsampled luminance representation of every frame:

- robust median background;
- median-absolute-deviation noise estimate;
- detected stellar peaks;
- approximate stellar FWHM;
- approximate ellipticity;
- high-pixel saturation fraction.

Thresholds are relative to the session where appropriate. The output is an
auditable CSV, not an irreversible deletion decision. A person should inspect
large or surprising rejection groups.

## Registration and integration

`stack` stages only approved files and runs a fixed Siril 1.4+ script. The
recipe debayers, performs two-pass registration, filters poor roundness and FWHM,
and integrates with rejection and additive scaling. It creates one 32-bit linear
FITS master used as the comparison boundary for all downstream branches.

## Linear and nonlinear boundaries

Gradient correction, color calibration, and the strongest noise reduction
should normally happen while data remain linear. Star separation is most useful
early when selected. Stretching, contrast, saturation, StarShrink, star
emphasis, and presentation color are nonlinear and subjective. Keeping that
boundary explicit makes alternative finishes cheap and prevents a display JPEG
from becoming the accidental master.

## External tools

SeestarFlow orchestrates external applications; it does not copy or embed their
code or models. Exact commands and input hashes are written to `recipe.json`.
Licenses, model downloads, GPU choice, and application updates remain the user's
responsibility.

The automated production branch uses the licensed stand-alone
NoiseXTerminator, plus optional StarXTerminator. GradientXTerminator and
StarShrink remain Photoshop decision gates. No BlurXTerminator license is
assumed.

## Safety properties

- Raw archives are copied and hash-verified.
- No pipeline stage edits files inside `originals/`.
- Stacking is staged into a timestamped product tree.
- Free and paid comparisons share an identical input hash.
- Dry-run mode shows external commands before execution.
- Generated images and third-party data are excluded from version control.
