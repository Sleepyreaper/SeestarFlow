# Capturing data the workflow can use

The most important setting is saving individual FITS frames. An app JPEG or a
single live stack cannot be quality-filtered and reintegrated in the same way.

## Required session settings

- Enable the Seestar option that saves every frame during enhancement.
- Use the telephoto camera at 1x; digital zoom adds no captured detail.
- Use EQ mode for long deep-sky runs and for any exposure duration that requires
  it on the installed firmware.
- Autofocus after the slew and again after meaningful temperature change.
- Image high in the sky, preferably around transit.
- Keep framing, filter, and exposure family consistent across nights.
- Use external power and dew control when conditions require them.
- Avoid walking near the tripod, especially on a flexible deck.

## Filter choice

Use dual-band for emission nebulae dominated by hydrogen-alpha and oxygen-III:
Veil, Rosette, North America, Heart, Soul, and Horsehead/IC 434.

Use the normal broadband/UV-IR-cut path for galaxies, reflection nebulae,
clusters, and natural star color. A dual-band filter discards much of the useful
continuum signal from those targets.

## 10, 30, and 60 seconds

At equal frame count, longer frames simply contain more total time. At equal
total integration, results can be much closer than expected once sky background
dominates read noise.

| 500 accepted frames | Total integration | Typical role |
| --- | ---: | --- |
| 10 seconds | 1 h 23 m 20 s | bright cores, imperfect tracking, HDR stars |
| 20 seconds | 2 h 46 m 40 s | middle ground when 30s keeper rate is weak |
| 30 seconds | 4 h 10 m | default EQ workhorse |
| 60 seconds | 8 h 20 m | faint signal under dark, stable EQ conditions |

Longer subs reduce file count and repeated read noise, but an unusable frame
loses more time and bright stars can saturate sooner. Satellite trails can often
be rejected at the pixel level during stacking; a trail does not automatically
invalidate its whole exposure. Compare equal clock time and equal final stacked
integration separately, with identical framing and filter. See
[the EQ and exposure field card](EQ_EXPOSURE_TEST.md) for the timed blocks,
measurements and executable selection tool.

EQ also reduces field rotation at 10 and 30 seconds. More consistent field
coverage and less edge cropping can justify the TH10 even when 60 seconds does
not improve central-image noise at a particular site. Extra filters are not
required for this benefit.

The official S50 Pro exposure menu adds 60 seconds only in EQ mode. Longer is
not automatically better: one failed 60-second sub loses six times the photons
of a failed 10-second sub. Compare accepted integration per clock hour.

## Storage

The S50 Pro is 128 GB with approximately 100 GB usable. One early real
2160-by-3840 telephoto FITS measured 16,594,560 bytes. Under the deliberately
conservative assumption of continuous capture at the same size:

| Exposure | Approximate raw storage per hour | Eight-hour raw total |
| --- | ---: | ---: |
| 10s | 5.97 GB | 47.8 GB |
| 20s | 2.99 GB | 23.9 GB |
| 30s | 1.99 GB | 15.9 GB |
| 60s | 1.00 GB | 8.0 GB |

These are planning numbers, not yet measurements of the owner's firmware and
wide-camera modes. Use `seestarflow storage` with the actual Monday file size.
Copy off and back up after every serious night.

## Multiple nights

Hours from different nights combine normally. Keep each night separately during
ingest so focus, transparency, and background changes remain measurable. Register
the accepted frames together only after inspecting per-night quality.

## Session notes

Record target, site label, start/end time, mount mode, exposure, filter, polar
alignment error, autofocus times, Moon, clouds, wind, dew, heater use, and any
tripod contact. Acquisition context often explains a rejection cluster faster
than another algorithm does.
