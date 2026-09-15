# TH10 and exposure comparison: field card and processing protocol

EQ is part of our production setup. It reduces field rotation even at 10 or
30 seconds, preserves more consistently exposed edges over time, and enables
60-second exposures. The initial Alt-Az run simply precedes the separately
shipped TH10 and plate. No additional filters or software purchase is required
for these tests; use the built-in filter appropriate to the selected target.

## Test A: Monday without the TH10 (40 minutes plus setup)

First complete a short 10-second live stack, focus, and verify individual FITS
saving. Then choose ONE clear target with enough sky remaining for 40 minutes.
Use M31/broadband if its northeast window is open, or an emission region with
the built-in LP filter. A target well clear of trees and the zenith is preferred.
If those conditions are unavailable, capture ordinary first-light data and log
why the controlled comparison was deferred.

| Block | Mount | Exposure | Clock time |
| --- | --- | ---: | ---: |
| A1 | Alt-Az | 10s | 10 minutes |
| B1 | Alt-Az | 30s | 10 minutes |
| B2 | Alt-Az | 30s | 10 minutes |
| A2 | Alt-Az | 10s | 10 minutes |

This gives 20 clock minutes per exposure; the bookended order balances a gradual
change in altitude or transparency. It does not eliminate clouds or all time
bias. Keep the same filter, camera, target, framing, focus and enhancement state.
Record start/stop times for each block to separate files later. Stop on frame
boundaries and record actual durations rather than silently rounding to ten.
If 30 seconds has poor star shapes, retain it as evidence and return to 10s.

## Test B: first clear night with TH10 (60 minutes plus setup)

Mount the TH10 and correct quick-release plate according to ZWO's instructions.
Use firm ground with the tripod low, secure the locks, and route cables with
slack. Switch to EQ through the app and complete its polar-alignment routine;
record the final residual and confirm it again after locking the head. Follow
the app's geometry rather than assuming a particular number on the head dial.

Choose one target with at least an hour of unobstructed motion, preferably
roughly 40–70 degrees high. Run autofocus and a short verification stack before
starting the timed experiment. This test needs no new filters: choose broadband
for M31 or the built-in LP filter for an emission nebula, then leave it fixed.

| Block | Mount | Exposure | Clock time |
| --- | --- | ---: | ---: |
| A1 | EQ | 30s | 15 minutes |
| B1 | EQ | 60s | 15 minutes |
| B2 | EQ | 60s | 15 minutes |
| A2 | EQ | 30s | 15 minutes |

Use the same setup, target, framing, camera, filter, gain (if controllable), and
focus for all four blocks. Start each block after autofocus/slew/setup completes.
Include normal capture overhead, dithers and rejected frames in clock time.
Log a cloud, gust, focus change, or interruption instead of erasing it. Repeat
with reversed exposure order on a later night to check whether the result holds.

Do not wait for a preset number of accepted frames: that would give the weaker
mode extra clock time and conceal lost imaging efficiency.

## Test C: isolate what EQ does (60 minutes plus mount changes)

Use 30-second exposures throughout, one target and filter, and blocks of
Alt-Az 15m -> EQ 15m -> EQ 15m -> Alt-Az 15m. Reinitialize and align after any
mount change. Log setup time separately: report both capture-only yield and the
time spent setting up. If mode changes cannot be done without a major framing
or focus change, run matched one-hour sessions on successive clear nights and
label that comparison as confounded by weather/seeing.

In addition to the common central crop, inspect the entire uncropped field.
Field rotation's edge penalty grows with time; a short test may show little.
A later 1–2-hour run per mode at similar sky positions is the stronger framing
test. Do not claim that a 15-minute result measures the entire EQ benefit.

## Record and transfer

For each block preserve the source FITS, app stack/JPEG, real elapsed seconds,
app-reported accepted seconds and rejection count if available, app/firmware
versions, alignment residual, focus changes, target/filter, and weather notes.
Use `templates/EXPOSURE_BLOCK_LOG.csv` as a field log; blank cells stay unknown.

Split copies of archived frames into separate block folders by the recorded
times. Preserve originals. Verify the timestamp timezone before splitting;
FITS timestamps may be UTC while the phone shows local time. Include only
individual telephoto subs, never the app masters. Each block needs an explicit
`approved.lst`, one filename per line, from reviewed QA. Review SeestarFlow's
automated rejection against Siril star inspection, particularly for small CFA
stars. A percentile estimate of saturation is not a count of clipped stars.

Copy `capture-comparison.example.json` next to the block folders and enter the
actual sources, exposure settings, mount labels and elapsed seconds. Then run:

```powershell
python -m seestarflow capture-compare --spec comparison/my-test.json --output comparison/my-test-report
```

Paths in the spec are relative to that spec, unless absolute. Use a fresh output
folder for each run. The command reads and hashes files without modifying them.
It produces `throughput.csv`, `report.json`, and absolute-path file lists for
each group's full QA selection and equal-integration selection. Equal-time
selections are spread through the capture interval instead of taking only its
first frames. Source paths are private local records; do not publish the report
unchanged if those paths identify a person or location.

The command validates exposure, frame geometry, target/filter/camera/gain where
available, and EQMODE when present. Missing metadata produces a warning and
requires the field log. It rejects RGB/stacked masters, truncated files,
duplicates, and impossible saved-integration totals. Header equality alone does
not prove matching atmospheric conditions, polar alignment or focus.

## How the resulting images will be compared

1. Build a stack from every QA-approved frame per group. These measure what the
   equal clock intervals actually delivered. All-frames lists are included.
2. Build a second set from the equal-integration lists. The duration is rounded
   down to a common multiple of exposure lengths. These isolate exposure length
   from total collected time. If Siril rejects additional frames, regenerate
   the selections using the final approved lists and recheck equal integration.
3. Register to a common reference/grid, normalize brightness using common
   unsaturated stars, and use one common crop and stretch. Record the reference
   and transform. Avoid independent automatic stretches for the comparison.
4. Measure FWHM/shape on the same unsaturated stars; inspect clipping using a
   verified sensor ceiling, not a percentile. Measure noise in matching blank
   regions, checking gradients and nebulosity do not dominate the measurement.
5. Show full-frame coverage as a separate comparison. Reject unexposed borders
   from noise measurements, but retain them in the coverage view. Masks must
   represent actual registration coverage; a zero pixel alone is not proof of
   missing coverage. Record any automatic reframing/mosaic behavior.
6. Inspect the linear/basic-stretch results before RC Astro. Apply identical
   GraXpert/RC Astro settings to a second pair, followed by a separately labeled
   Photoshop showcase. Do not let smoothing conceal an acquisition defect.
7. Export an image sheet with app view, equal-clock stack, equal-integration
   stack, target crop, bright-star crop and final finish. Label every panel with
   mount, exposure, actual stacked count/time and processing branch.

Acquisition yield alone does not decide the winner. If 60 seconds preserves
more credible faint detail with satisfactory stars, choose it for that target
and sky. If 30 seconds preserves bright stars or has better useful throughput,
choose 30 seconds in EQ and retain EQ's field-orientation benefit. A tie means
either is suitable there; fewer files may favor 60 seconds. Test again under
dark skies and with the LP filter before generalizing to all targets.

The current command prepares and audits selections. It does not automatically
run Siril, estimate final-stack SNR, or render the image sheet. Those steps need
actual matched captures and verified final rejection/coverage information.

## Evidence and corrections

- The public IC 1396A download we possess contains three sample subs and a
  supplied integration. It does not validate a 1,267-frame Pro raw stack.
- The earlier DSLR Horsehead result has unresolved calibration/background
  issues. It cannot establish what an hour of good data would look like.
- No verified matched Pro 30/60s or EQ/Alt-Az raw pair was found in the renewed
  public search on 2026-09-13. The first hardware comparison remains pending.

References: [ZWO S50 Pro exposure/mount specifications](https://www.seestar.com/de/products/seestar-s50-pro-smart-telescope),
[photographer's S50 Pro EQ report hosted by ZWO](https://us.seestar.com/blogs/review/one-smart-telescope-four-worlds-milky-way-solar-deep-sky-scenery-with-the-seestar-s50-pro),
[SharpCap exposure guidance](https://docs.sharpcap.co.uk/4.1/6_GettingGoodImages.htm),
[IC 1396A source article](https://www.blickohnegrenzen.de/2026/09/07/s50-pro-test-tag-11-12-siril-premiere-az-vs-eq/).
