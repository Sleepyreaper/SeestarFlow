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
| 30 seconds | 4 h 10 m | default EQ workhorse |
| 60 seconds | 8 h 20 m | faint signal under dark, stable EQ conditions |

Longer subs reduce file count and repeated read noise but increase the cost of a
gust, cloud, satellite, tracking error, or saturated star. Test rather than
guess: capture 30 frames at each available duration with identical framing and
filter, then compare keeper rate, FWHM, ellipticity, background, saturation, and
signal-to-noise per minute.

## Multiple nights

Hours from different nights combine normally. Keep each night separately during
ingest so focus, transparency, and background changes remain measurable. Register
the accepted frames together only after inspecting per-night quality.

## Session notes

Record target, site label, start/end time, mount mode, exposure, filter, polar
alignment error, autofocus times, Moon, clouds, wind, dew, heater use, and any
tripod contact. Acquisition context often explains a rejection cluster faster
than another algorithm does.
