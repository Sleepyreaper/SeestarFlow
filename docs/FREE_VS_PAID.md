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

## Paid production branch

```text
same linear master
  -> GraXpert background extraction (no denoise)
  -> BlurXTerminator while linear
  -> NoiseXTerminator once while linear
  -> optional StarXTerminator
  -> Siril stretch and color preparation
  -> separate star and object treatment when justified
  -> layered Photoshop recombination and local finish
  -> Lightroom catalog, release variants, and print soft proof
  -> TIFF + JPEG
```

This is the stack already purchased and proven on the IC 1396A benchmark. It is
complete without PixInsight. PixInsight remains a possible future specialist
tool for LocalNormalization, complex mosaics, HDR/channel composition, image
containers, and PixelMath—not a prerequisite for excellent S50 Pro work.

RC Astro tools add astronomy-specific learned correction:

- BlurXTerminator: optical deconvolution and stellar-profile correction.
- NoiseXTerminator: learned noise reduction.
- StarXTerminator: star/object separation.

Treat their output as a hypothesis that must survive visual inspection. On dense,
undersampled star fields, separation can leave soft aureoles or false residuals.
If the stars-intact result is more credible, keep it.

## Purchase decision

The production software is already purchased: Siril, GraXpert, RC Astro,
Photoshop, and Lightroom. Do not buy more software for Monday. Add PixInsight
only when a documented limitation—not curiosity—survives three real projects.

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
