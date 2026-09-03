# Free stack versus paid stack

The free and paid branches solve different problems. Paid software cannot create
signal that was never captured, and a deeper integration usually matters more
than changing applications.

## Shared foundation

Both branches use:

1. individual FITS acquisition;
2. immutable, hashed ingest;
3. measured frame rejection;
4. registration and integration;
5. the identical 32-bit linear master.

Changing the source master invalidates a software comparison.

## Free branch

```text
Siril integration
  -> crop registration borders
  -> GraXpert background extraction
  -> Siril plate solve and PCC where appropriate
  -> GraXpert denoise or restrained Siril denoise
  -> optional StarNet/Siril separation
  -> controlled stretch
  -> TIFF + JPEG
```

This branch can produce excellent work. Its strengths are automation, low cost,
scriptability, and a clear path from subframes to final export.

## Paid branch

```text
same linear master
  -> PixInsight background/color tools
  -> BlurXTerminator while linear
  -> NoiseXTerminator or GraXpert while linear
  -> optional StarXTerminator
  -> masks / GHS or HistogramTransformation
  -> separate star and object treatment when justified
  -> PixelMath recombination
  -> TIFF + JPEG
```

PixInsight's advantage is not one magic filter. It is control: repeatable process
icons and scripts, masks, image containers, LocalNormalization, sophisticated
color workflows, HDR composition, PixelMath, and exact management of intermediate
linear products.

RC Astro tools add astronomy-specific learned correction:

- BlurXTerminator: optical deconvolution and stellar-profile correction.
- NoiseXTerminator: learned noise reduction.
- StarXTerminator: star/object separation.

Treat their output as a hypothesis that must survive visual inspection. On dense,
undersampled star fields, separation can leave soft aureoles or false residuals.
If the stars-intact result is more credible, keep it.

## Recommended purchase order

1. Learn the free stack and obtain reliable capture data.
2. Add PixInsight when masks, multi-night management, HDR, and reproducibility
   become the limitation.
3. Trial BlurXTerminator on the same linear masters.
4. Add NoiseXTerminator or StarXTerminator only when matched tests show a useful
   improvement over GraXpert and the free separation options.

Prices and bundles change; this repository intentionally does not hardcode them.

## What paid software cannot fix

- too little integration;
- saturated cores with no shorter exposure set;
- persistent tracking trails;
- lost raw frames;
- dew-softened optics;
- severe field rotation;
- incorrect filter choice;
- clipped or heavily processed app-only output.
