# Seestar app field card

This is the short checklist to open on the phone before every deep-sky session.
Menu labels can move between firmware releases; preserve the intent when they do.

## Production defaults: stock Alt-Az

| Setting | Value | Why |
| --- | --- | --- |
| Expert mode | On | exposes the capture controls |
| Live View Format | RAW | preserves the strongest live/stack data path |
| Enhance EXP | 10 s | dependable Alt-Az baseline |
| Execute enhancement after GOTO | Off | allows framing/filter/focus check first |
| Skip horizontal calibration | Off | lets the telescope build the needed model |
| Auto LP Filter | Off | makes filter choice deliberate |
| Save each frame | On | creates individual FITS for reprocessing |
| Auto Focus | On | starting point; refocus after temperature change |
| Trail rejection | On | rejects obvious moving trails when possible |
| Dark correction | On | applies the device calibration path |
| Full screen mode | Optional | presentation only; no data-quality effect |

## Choose the filter from the object

- **LP on:** emission nebulae such as M27, North America, Veil, Heart, Soul,
  Rosette, and Orion's emission regions in bright sky.
- **LP off / IRCUT:** galaxies, open or globular clusters, reflection nebulae,
  dark nebulae, and natural-color star fields.
- At a dark site, test both on emission targets. LP can improve line-emission
  contrast, while broadband preserves star color and continuum signal.
- Auto LP remains off during controlled tests so the app cannot silently change
  the variable.

## Literal start sequence

1. Stabilize and roughly level the tripod; attach and power on the Seestar.
2. Connect in the app and verify the settings above.
3. Select a target that is clear of the local horizon mask.
4. Tap GOTO and allow plate solving/horizontal calibration to finish.
5. Leave enhancement stopped. Choose LP on or off deliberately.
6. Tap Focus and wait for autofocus to complete.
7. Start enhancement for two minutes.
8. Confirm round stars, stable framing, the expected object, and rising stack
   time. Confirm **Save each frame** is still on.
9. Continue the planned block. Do not keep changing the live stretch.
10. Stop enhancement before selecting the next target.

## What to inspect at 2, 15, and 60 minutes

- **2 min:** correct target, focus, framing, no tree/roof incursion, no bright
  flare or obvious tracking failure.
- **15 min:** target structure and color are emerging; stars remain round; stack
  time continues to increase. A satellite trail in the preview is not, by
  itself, proof that the entire raw frame set is ruined.
- **60 min:** compare fine structure and background smoothness with the 15-minute
  screenshot. If it is improving, continue the hero target instead of hopping.

The displayed timer is accepted stack integration, not necessarily wall-clock
time. Record both when testing efficiency.

## Dew, power, and light

- Enable the anti-dew/heater control when ambient temperature approaches the
  dew point or moisture appears. Recheck after firmware updates because the app
  may not preserve every setting.
- Keep external power and cable strain away from the rotating body.
- A light shield may block direct lamp rays, but must remain clear of the moving
  telescope, vents, and sky path. Do not wrap the telescope in cardboard.
- Stop if the optical window fogs; heating prevents dew better than it cures a
  soaked surface.

## Closing sequence

1. Stop enhancement and wait for the current exposure to finish.
2. Save/share the app preview if wanted for outreach.
3. Stow the telescope from the app.
4. Power off, bring it inside, and let surface moisture evaporate before sealing
   it in a case.
5. Connect by USB-C, copy each target folder and `_sub` folder, then follow
   [OPERATING_PLAYBOOK.md](OPERATING_PLAYBOOK.md).

## EQ changes

Use the TH10 only after a successful stock-tripod session. Level the tripod,
point the designated leg north, set the latitude tilt, enable EQ mode, and align
within 1 degree. Begin with 30 seconds; test 60 seconds rather than assuming it
is better. The complete controlled protocol is in
[EQ_EXPOSURE_TEST.md](EQ_EXPOSURE_TEST.md).
