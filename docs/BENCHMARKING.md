# Benchmarking processing changes

Astrophotography comparisons are easy to bias. This protocol tests tools against
the same photons and requires failures to remain visible.

For changes in capture settings, use [EQ_EXPOSURE_TEST.md](EQ_EXPOSURE_TEST.md).
That experiment separately compares equal clock time, equal final integration,
and field coverage. The `capture-compare` command audits raw input and produces
matched file selections; image-quality conclusions require the actual stacks.

## Freeze the input

Record the SHA-256 of the common linear FITS master. Every branch must use that
file, the same orientation, and the same crop coordinates. Do not compare a short
free integration with a longer paid integration.

## Export matched views

For every branch create:

- a full-frame image at identical dimensions;
- a native-resolution central or target crop with no rescaling;
- a bright-star crop that exposes halos and ringing;
- a low-signal crop that exposes noise texture and background damage;
- a 16-bit TIFF and a display JPEG;
- a machine-readable recipe with versions and parameters.

## Measurements

Compare:

- stellar FWHM and eccentricity;
- clipped-pixel count;
- background median and robust noise;
- local contrast in known structures;
- chromatic halos and color blotching;
- separation residuals;
- runtime and peak storage.

## Acceptance criteria

A processing change is accepted only when it improves at least one intended
property without materially damaging another. Examples:

- smaller stars are not an improvement if they acquire dark ringing;
- smoother background is not an improvement if faint dust disappears;
- more colorful nebulosity is not an improvement if neutral background becomes
  strongly tinted by a bad calibration reference;
- a starless image is not an improvement if it contains soft aureole ghosts;
- sharpening is not an improvement if repeated texture appears where the linear
  master has no supporting signal.

## Keep rejected experiments

Record the reason an experiment was rejected. A failed automatic color
calibration or star-separation pass teaches which field conditions violate the
method's assumptions and prevents the mistake from returning silently.

## Public-data ethics

Keep a provenance note with source URL, author, acquisition metadata, license,
and restrictions. Do not redistribute a dataset merely because it was publicly
downloadable. Exclude all third-party FITS data and derived images from this
repository; publish only the workflow unless the license and author explicitly
permit redistribution.
