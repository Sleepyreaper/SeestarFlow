# S50 Pro first-night runbook — Monday, September 14, 2026

Monday has two success criteria:

1. show a compelling live image in 10–15 minutes; and
2. bring home enough individual FITS files to prove the complete production
   workflow.

If both happen, the night is a complete success. A sale-ready print is not the
commissioning criterion.

## Preferred physical setup

Use the normal Dob/driveway area on the ground, shifted just far enough that the
house, a vehicle, or a temporary opaque panel blocks direct sight of the street
lamp from both S50 Pro lenses. Preserve the high-sky opening and a safe path for
cars and pedestrians.

Do **not** put the S50 Pro on a truck roof. Sheet metal flex, suspension motion,
warm-engine currents, dew, and fall risk outweigh the extra few feet of height.
Use the supplied tripod Monday. Use the neighbor's driveway only with permission
and while supervised; its western opening is an optional outreach position, not
the primary data position.

Monday is Alt-Az. The separately shipped TH10 and quick-release plate begin the
EQ learning phase after the basic telescope is proven.

EQ is part of the intended production setup. After the short first-light stack,
if a single target has a clear 40-minute window, replace one extended target
block below with the 10/30-second experiment in [EQ_EXPOSURE_TEST.md](EQ_EXPOSURE_TEST.md).
When the TH10 arrives, run its 30/60-second EQ experiment and then the separate
same-exposure mount comparison. These are planned tests, not optional hardware
benefits we have already dismissed.

## Before delivery / have ready

- current Seestar app installed and signed into the correct ZWO account;
- phone/tablet charged, location/Bluetooth/local-network permissions available;
- Anker power bank and a known-good USB-C cable;
- red headlamp, small towel, lens-safe air blower, folding chair;
- laptop and included USB-C **data** cable indoors for transfer;
- an opaque, nonreflective lamp shield or black foam-board panel with secure
  weights/clamps; never drape anything over the telescope;
- a fresh copy of `docs/templates/SESSION_NOTES.md` or the checklist below.

## Delivery-day daylight sequence

Complete this before 6:30 p.m.; do not learn activation during astronomical
darkness.

1. Photograph the unopened box if shipping damage is visible.
2. Inventory telescope, carbon tripod, solar filter, cable, case, guides, and
   lens openings. Do not test solar mode without the supplied solar filter.
3. Fully charge the scope. The manual permits operation while charging, but the
   advertised nine-hour test was at 25°C with the dew heater off; real runtime
   can be lower.
4. Mount the scope to the supplied 3/8-inch tripod on the floor. Power on using
   the first-use sequence: short press about one second, then hold about two
   seconds.
5. Activate online, connect, and complete any firmware update. Let it reboot.
6. Record app version, firmware, reported free storage, and battery percentage.
7. Find these controls without changing targets: Stargazing, SkyAtlas/Tonight's
   Best, filter selection, exposure, autofocus, dew heater, Plan Mode, Advanced
   Settings, **Save Each Frame**, album, and shutdown/home position.
8. Set **Save Each Frame ON**. Re-check it inside the active imaging screen's
   menu before the serious run; firmware UI placement may differ.
9. Test that the phone remains connected from the intended indoor chair/window.
   The official range specification is up to 10 m only under open ideal
   conditions, so a wall can reduce it substantially.
10. Leave at least 70 GB free for commissioning. The official device is 128 GB
    with about 100 GB usable.

## 7:45–8:35 p.m. outdoor commissioning

- Put the tripod at minimum practical height, legs fully spread, on hard ground.
- Make the top stable and level using the app indication; do not level by eye.
- Turn off house and landscape lights. Block direct lamp light at the telescope,
  not merely at the observer.
- Initialize/compass-calibrate only as the app requests, then GOTO a bright
  star or first target and confirm plate solving.
- Run autofocus after the telescope has been outside about 10–15 minutes.
- Take one ordinary wide-camera still to document the site and obstruction
  pattern. This is evidence, not an artistic exposure.
- Start a two-minute test stack and confirm stars are round and the accepted
  integration counter advances.

## The exact Monday queue

Clock times are flexible. Accepted integration matters more than elapsed time.

| Order / window | Target | Approximate sky position | Capture | Goal | Switch/stop rule |
| --- | --- | --- | --- | --- | --- |
| 1 / 8:40–9:00 | M27 Dumbbell Nebula | 77–79° high, near south | 10s, dual-band, 12–15 accepted min | Fast live “wow,” focus and emission test | If GOTO/stack fails twice, use M52 for commissioning |
| 2 / 9:05–9:35 | NGC 7000 North America Nebula | roughly 75–80° high, east/northeast | 10s, dual-band, 25–30 accepted min | Extended faint signal, gradient and star-separation test | Frame a recognizable high-contrast region; no mosaic Monday |
| 3 / 9:45–10:30 | M31 Andromeda | roughly 40–50° high, northeast/east-northeast | 10s, broadband, 30–45 accepted min | Galaxy color/background master and Moon-after-set test | Use the verified NE/east opening; if blocked, extend NGC 7000 |
| Optional / after 10:30 | M52 | roughly 50° high, northeast | 10s, broadband, 10 accepted min | Star-color/cluster control image | Only if visible and time/energy remain |

Why M27 first: it is bright, compact, high enough for clean city capture, and
responds well to the built-in dual-band filter. It is a stronger first public
demonstration than spending the same 12 minutes on a faint broadband galaxy.
NGC 7000 tests the sort of extended nebula processing we want to master. M31 is
the broadband control after the roughly 15%-illuminated crescent Moon sets around
9:29 p.m. local time.

The western Veil is a high-priority future showpiece, but it passes close to the
zenith during this window. Monday's M27/NGC 7000 pair is less likely to turn the
first evening into an Alt-Az zenith-tracking experiment. If the app recommends a
well-framed Veil segment and it is below about 80° altitude, a supervised
10-minute preview may replace M52—not one of the two science runs.

## What to show friends and neighbors

Let M27 accumulate for five minutes before judging it. At 10–15 accepted minutes:

- show the live stack and then the sky map so they can understand where it is;
- avoid dragging every enhancement slider to maximum;
- save one app-rendered JPEG as the outreach record;
- tell them the color is accumulated camera data, not what a dark-adapted eye
  would see instantly through an eyepiece;
- keep the raw FITS running—outreach does not replace the source data.

## Dew and weather gate

The forecast remains provisional. A current public forecast leans hazy with
very high late-night humidity and a dew point near the low 70s, so dual-band
nebulae are safer than ambitious broadband faint dust. Re-check at 5 p.m. and
again immediately before setup.

Proceed only if radar is dry, no thunder is nearby, the equipment will remain
within the manual's temperature/humidity limits, and wind is modest. Enable the
built-in dew heater when the dew-point spread becomes small or the front optic
begins to soften; connect the power bank because heater use reduces runtime.
Stop for condensation on electronics, rain, or a rapidly worsening forecast.

## Before going inside

- The scope is on stable ground, not in a road/sidewalk path.
- No vehicle can enter the driveway without moving it.
- Direct lamp light is blocked from the lenses.
- Live stack has advanced for at least five accepted minutes.
- Wi-Fi is reliable at the indoor viewing position.
- Power cable has slack and cannot pull or trip the unit.
- Finish time is explicit. Monday is supervised; do not leave it outside all
  night.

## End-of-night transfer — do not skip

1. Stop capture and command home/shutdown through the app.
2. Bring the dry telescope indoors capped/cased as the manual instructs. If the
   surface is damp, let it acclimate in a dry protected area before sealing.
3. Connect by the included USB-C data cable and copy the entire target folders,
   including each `_sub` folder and app/device stack.
4. Record counts and measure one FITS file size. Run:

```powershell
python -m seestarflow storage --exposure 10 --hours 8
python -m seestarflow ingest `
  --source "E:/MyWorks/M27_sub" `
  --target M27 `
  --site north-atlanta-backyard `
  --filter dualband `
  --mount altaz
```

5. Confirm `manifest.json`, open several archived FITS files, and make a second
   backup before deleting anything from the telescope.
6. Send the untouched target folder to the processing machine. The first real
   comparison uses the same accepted photons for app, free, and paid results.

## Monday's scorecard

- [ ] Device activated and firmware/app versions recorded.
- [ ] Reported storage and battery recorded.
- [ ] Save Each Frame verified and real `_sub` FITS recovered.
- [ ] One 10–15 minute M27 live result saved.
- [ ] One 25–30 minute dual-band extended target captured.
- [ ] One 30–45 minute broadband target captured, or documented obstruction.
- [ ] Rejection/acceptance behavior observed.
- [ ] Indoor connection range tested.
- [ ] Raw files transferred, hashed, and backed up twice.
- [ ] No exact home address or GPS included in public metadata.

Monday needs no additional software or major hardware purchase. See
`EQUIPMENT_AND_STORAGE.md` for the two-drive plan required before full-night or
travel capture.

## Sources

- [S50 Pro official product page](https://us.seestar.com/products/seestar-s50-pro-smart-telescope)
- [S50 Pro V1 user manual](https://cdn.shopify.com/s/files/1/0735/7061/5396/files/Seestar_S50_Pro_User_Manual_EN.pdf?v=1787535789)
- [ZWO Save Each Frame and `_sub` folder explanation](https://us.seestar.com/blogs/tutorial/simulated-stargazing)
- [ZWO USB-C and app file-transfer guide](https://us.seestar.com/blogs/tutorial/seestar-file-storage-download-guide)
- [Atlanta Moon data for September 2026](https://www.timeanddate.com/moon/usa/atlanta?month=9)
