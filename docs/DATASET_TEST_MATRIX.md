# Dataset test matrix

## Decision

Do not collect data merely because it is astronomical or visually impressive.
Add a dataset only when it exercises a missing acquisition, calibration, target,
or processing condition. The S50 Pro workflow is validated in the following
order:

1. **Our S50 Pro individual FITS** are the hardware truth.
2. **Public S50 Pro individual FITS** are the closest external regression data.
3. **Original S50 individual FITS** are the best abundant Seestar ingest,
   registration, rejection, and multi-night proxy.
4. **S30 Pro FITS masters** are useful for 4K, wide-field, undersampled-star,
   and final-edit tests, but cannot validate raw-frame QA or stacking.
5. **Conventional one-shot-color data** are useful for calibration frames,
   long exposures, deeper signal, and difficult gradients. They do not predict
   what an S50 Pro can capture.
6. **Mono narrowband data** are useful later for channel combination and
   creative color mapping only. They are not an S50 Pro proxy.

Original S50 data ranks ahead of S30 Pro data when the question is “will our
Monday ingest and stack work?” The S30 Pro ranks ahead when the question is
“will our 4K Pro finishing technique survive a wide field and small stars?”

## Coverage grid

| Test cell | Current dataset | Input type | Status | What it proves |
| --- | --- | --- | --- | --- |
| S50 Pro, individual 10-second subs | IC 1396A, three sample frames | Individual FITS | Headers inspected only | Pro dimensions and metadata; insufficient for stacking/rejection validation |
| S50 Pro, integrated master | IC 1396A, supplied Siril result | Integrated FITS | Finishing completed | GraXpert/RC Astro/Siril/Photoshop handoff; original integration was the reviewer's |
| S50 Pro, our first-night data | M27, NGC 7331, M52 | Individual FITS plus app masters | Captured; ingest/finishing regression active | Our exact optics, firmware, focus, site, file size, filter, and sub-length behavior |
| Original S50, broadband galaxy | M51, M63, M101 | Individual FITS | Complete | Small-galaxy QA, registration, restrained sharpening |
| Original S50, emission nebula | NGC 6995, M42, M27, Bubble, Pacman | Individual FITS | Complete | LP-filter color, faint nebulosity, HDR core, multi-night stacking |
| Original S50, reflection/dark dust | NGC 7023 Iris | Individual FITS | Complete | Broadband dust, gradient restraint, multi-night combination |
| Original S50, cluster | M13 | Individual FITS | Complete | Stellar profiles, color, deconvolution and star-control limits |
| S30 Pro, broadband wide galaxy | M31, 268 x 20 seconds | Integrated RGB FITS | Complete | 4K wide-field galaxy finishing; not raw ingest |
| S30 Pro, emission nebula | NGC 3372, 634 x 10 seconds | Integrated RGB FITS | Complete | Dense 4K nebula field and star separation; not raw ingest |
| S30 Pro, wide-camera Milky Way | Milky Way, 33 x 30 seconds | Integrated RGB FITS | Diagnostic complete | Very wide field and short integration; not telephoto/raw ingest |
| S30 Pro, individual subs | No open, verified download found as of 2026-09-12 | Individual FITS | Open | Would test S30 Pro registration and rejection; low priority after Monday |
| DSLR OSC, complete calibration set | Horsehead/Flame, Canon EOS 40Da | 63 lights plus darks/flats/biases | Complete with caveat | Calibration metadata validation and recovery from suspect calibration folders |
| Cooled OSC, long-sub faint target | Prefer ASI533MC/ASI2600MC with lights/darks/flats | Individual FITS | Next optional acquisition | Clean cooled-camera calibration, long-sub gradients, faint-signal discipline |
| Mono SHO | None selected | Calibrated mono channels | Deferred | Palette/channel workflow only; not needed for first S50 Pro production |

## Public S50 Pro scan — 2026-09-12

Correction after local audit on 2026-09-13: the IC 1396A download contains only
THREE sample subs plus the reviewer's integrated master. The article discusses
a 1,267-frame project; we did not download or independently stack those 1,267
frames. Earlier claims that our complete S50 Pro raw stacking had been validated
were incorrect. No complete matched EQ/Alt-Az or 30/60-second Pro raw collection
was verified in the renewed search. New photographs alone do not close that gap.

The IC 1396A source and download are documented in the independent
[S50 Pro Siril/AZ test](https://www.blickohnegrenzen.de/2026/09/07/s50-pro-test-tag-11-12-siril-premiere-az-vs-eq/).
The original-S50 individual-sub library comes from the
[3AM Astro FIT portal](https://www.3amastro.com/) and is licensed CC BY-NC 4.0.

This is not a reason to substitute unrelated equipment and call it equivalent.
Our first saved frames are now the most relevant benchmark in the library. The
external sets remain useful for regression and for conditions not yet captured.

The app's **Save every frame** switch must be enabled inside each live-stacking
session. Verify that individual FITS exist after the first few accepted frames.

## S30 Pro finding

The current open search found no new, verified, directly downloadable S30 Pro
individual-sub collection. The three already downloaded S30 Pro files are
integrated RGB masters:

| Target | Header evidence | Use |
| --- | --- | --- |
| NGC 3372 Carina | `STACKCNT=634`, `EXPTIME=10`, `LIVETIME=6340` | 1h45m40s LP-filter 4K/drizzled finishing test |
| M31 Andromeda | `STACKCNT=268`, `EXPTIME=20`, `TOTALEXP=5360`, `EQMODE=0` | 1h29m20s broadband wide-galaxy finishing test |
| Milky Way | `STACKCNT=33`, `EXPTIME=30`, `TOTALEXP=990`, wide camera | 16m30s very-wide-field diagnostic |

Carina was shared in the photographer's
[S30 Pro raw-file post](https://www.reddit.com/r/seestar/comments/1s7772u/ngc_3372_carina_nebula_s30_pro_raw_file/).
The M31 and Milky Way masters came from the
[ZWO S30 Pro post-processing challenge](https://www.lovecpokladu.cz/en/home/competition-for-a-seestar-s30-pro-smart-telescope-10359).

Never debayer these RGB masters again, even if a stale Bayer keyword appears in
the header. They cannot measure frame acceptance, field rotation, registration,
or the benefit of 10 versus 20 versus 30-second individual subs.

## Conventional-camera Horsehead benchmark — 2026-09-12

Source: [Santiago Rodriguez's DSLR astronomy datasets](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html),
Horsehead Nebula archive. The archive contains Canon EOS 40Da CR2 files acquired
through a Sky-Watcher 72ED:

- 63 lights at ISO 800 and 60 seconds: 63 minutes total;
- 17 darks at ISO 800 and 60 seconds;
- 17 flats at ISO 100 and 2.5 seconds;
- 11 files in the bias folder.

Archive SHA-256:
`48E3744EA5A6F8BF6016260D23FEBA8C279CBDD27926CA7FC1EAE2DA7A7D9CDB`.

The metadata gate found that the bias folder was not homogeneous: its first
inspected file reported ISO 800 and 60 seconds, while its last reported ISO 800
and 1 second. The flats also used a different ISO from the lights. A blind
“lights + darks + flats + biases” run therefore was not accepted as the trusted
result.

The recovery stack used all 63 lights and the 17 matching darks. Siril registered
and integrated all 63 lights. A GraXpert run on the large DSLR stack did not
produce a valid output, and an experimental RBF background extraction overfit
the field, so both were rejected for the final. The historical retained pass
used a temporary tool configuration:

`dark-calibrated stack -> crop -> BlurXTerminator -> NoiseXTerminator once ->`
`StarXTerminator -> independent restrained stretches -> star recombination`

That line documents what produced that benchmark; it is not the current owned
baseline. The canonical production workflow does not assume BlurXTerminator.

The preview reveals the Flame and Horsehead but retains substantial background
and calibration problems. It is a troubleshooting result. Its weak appearance
does not establish a one-hour physical signal limit or an S50 Pro performance
forecast. Extra integration cannot be used as the explanation until calibration,
color balance, gradient correction, and stretching have been resolved.

The source site reserves copyright unless a dataset states otherwise. Keep this
benchmark private and noncommercial. It must never enter our portfolio, prints,
or sales catalog.

## Next external dataset, if needed

The next useful addition is not another integrated master. It is a rights-clear
cooled OSC dataset with individual lights and matched darks, flats, and biases,
preferably from an ASI533MC Pro or ASI2600MC Pro on a faint broadband target.
That would exercise the one major workflow cell still absent: reliable full
calibration of clean, long, cooled-camera subframes.

One candidate is the [Los Colores Invisibles project](https://www.cloudynights.com/forums/topic/972932-free-deep-sky-fits-files-for-processing-%E2%80%94-los-colores-invisibles-project/),
which advertises lights, darks, flats, biases, and masters from a 200PDS and
ASI533MC Pro. Access requires a free subscription and the files cannot be
redistributed; processed images require source credit. Do not sign up or publish
anything until those exact terms are reviewed at download time.

## Monday capture implications

- Begin in Alt-Az with 10-second subs. This is the lowest-risk systems test.
- Save every individual FITS and retain the app master for the live-show result.
- Capture a short broadband target and a short LP-filter emission target.
- Record attempted time, accepted integration, rejected-frame count, exposure,
  filter, temperature, location, and obstruction notes.
- After the short 10-second commissioning baseline, run the supervised 10/30s
  comparison in `EQ_EXPOSURE_TEST.md` if the target clears the local obstructions.
- When the TH10/EQ setup arrives, run the planned 30/60s comparison. EQ is part
  of the production plan, including when the chosen exposure is 30 seconds.
- Never mix exposure/filter families merely because the target name matches.
  Preserve them as separate sessions; combine only after inspection.

## Acceptance rule

A new dataset enters the regression library only if all of these are true:

1. source and rights are recorded;
2. raw individual frames or the limitation “integrated master” is explicit;
3. capture equipment and exposure metadata are recorded without invention;
4. archive SHA-256 is stored;
5. the dataset fills an open matrix cell;
6. output is visually checked at full frame and 100 percent;
7. rejected processing variants remain documented rather than silently hidden.
