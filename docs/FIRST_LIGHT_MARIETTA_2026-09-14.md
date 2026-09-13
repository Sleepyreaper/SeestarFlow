# S50 Pro first-light plan — Marietta, Georgia

For the final supervised delivery-day sequence, use [the first-night runbook](FIRST_NIGHT_RUNBOOK.md). It supersedes the target sequence below; this document retains the general commissioning checklists.

Planned arrival: Monday, September 14, 2026
Planning location: private Marietta driveway site (street address intentionally omitted)
Primary objective: verify the complete capture-to-processing workflow, not maximize one finished image.
Operating policy: supervised short sessions; no unattended all-night backyard operation is required.

## Success criteria

By the end of the first usable night we should have:

- a physically undamaged, activated, updated, and fully charged S50 Pro;
- a repeatable setup location and a photographed horizon profile;
- successful pointing, autofocus, tracking, and live stacking;
- individual telephoto FITS subframes saved, if the current app exposes that option;
- a native Seestar stack plus the matching individual subframes copied to the PC;
- one short broadband dataset and one short dual-band dataset;
- a session log containing the actual firmware, app version, storage, settings, sky direction, and failures.

## Before delivery

- Install/update the Seestar app and sign in to the intended ZWO account.
- Make at least 15 GB free on the phone/tablet.
- Prepare a reputable USB-C power source. The S50 Pro accepts 5 V/3 A or 12 V/3 A and can operate while charging.
- Prepare a USB-C data cable for the Windows offload test; the bundled cable should be tried first.
- Put a bubble level, microfiber-free optical air blower, red flashlight, extension cord/power bank, and weather cover nearby. The cover is for emergency removal only, not unattended rain operation.
- Do not buy an EQ wedge solely for first light. Prove the Alt-Az unit first.

## Delivery inspection — before nightfall

1. Photograph every side of the unopened shipping box and any dents, punctures, or water marks.
2. Open carefully and keep all packaging.
3. Inventory the S50 Pro, protective case, solar filter, USB-C cable, tripod, safety sheet, quick guide, and stickers.
4. Inspect the housing, tripod threads, lenses, USB-C port, filter, and case without touching optical surfaces.
5. Photograph any defect immediately. The current manual asks for evidence of shipping damage within three days.
6. Charge to 100% before the first long session.

## Daylight commissioning

1. Mount the scope on the supplied tripod on a stable surface and use the widest leg stance.
2. Power on for the first time: press for about one second, then press and hold for about two seconds.
3. Connect with Bluetooth/device/network permissions enabled.
4. Activate while the phone has Internet access and is signed into the ZWO account.
5. Install any offered firmware update without interrupting power; allow the automatic reboot.
6. Record:
   - serial number privately;
   - app version;
   - firmware version;
   - total and free storage reported by the device;
   - whether the device reports 128 GB or something different;
   - available exposure lengths in Alt-Az and EQ modes;
   - the exact name/location of the option that saves individual frames.
7. Test Scenery mode on a distant terrestrial object, both wide and telephoto cameras, and normal shutdown.
8. Test Station Mode on home Wi-Fi if it is useful at the setup point.
9. Connect to the Windows computer by USB and document the folders/file types exposed. Copy, do not move, the test files.

Never aim at the Sun during these tests. Solar work happens only with the supplied filter securely installed and the app's solar procedure followed.

## Horizon survey

### Provisional survey received September 8

The images were taken in chronological order: IMG_3176 north, IMG_3177 west, IMG_3178 south, and IMG_3179 east.

- **North:** best opening. Broad clear sky through north and likely northeast, with tall trees intruding from the left and lower horizon clutter from neighboring trees and houses.
- **West:** heavily obstructed by close trees and a neighboring house. Only a narrow high-altitude opening is dependable.
- **South:** heavily obstructed by trees, with a small high-altitude opening. Do not schedule low southern targets from this footprint.
- **East:** the garage wall and roof dominate. Low and mid-altitude eastern targets are unavailable until they climb above the roof or move into the northern/high-altitude opening.

The phone was pointed upward and the true horizon is outside most frames, so these are directional classifications rather than measured obstruction altitudes. A nighttime plate-solve test will establish the usable altitude floor. The first observing plan should favor north/northeast targets and avoid west/south targets.

### Night survey and candidate positions

A second chronological set established: IMG_3180 west, IMG_3181 east, and IMG_3182 the normal Dobsonian setup position. These source photographs remain private and are not copied into the repository because identifying property details are visible.

- **West from the sidewalk/driveway:** unsuitable. The nearby streetlight is directly visible, produces severe flare across the phone image, and is combined with substantial tree obstruction.
- **East from the sidewalk/driveway:** useful short-session window. There is a broad opening down the street between tree lines, though the low eastern horizon remains bright and the position is exposed to pedestrians, vehicles, headlights, and equipment risk.
- **Normal Dobsonian position:** preferred supervised home position. The house and trees form a high overhead corridor, the user-controlled exterior/landscape lights can be switched off, and the equipment remains farther from the street. Confirm at night whether the streetlight bulb itself is hidden from the S50 Pro lenses.

Use two named site profiles rather than pretending the yard has one horizon:

1. `backyard_dob_spot` — primary position for high-altitude north/overhead targets and routine supervised sessions.
2. `driveway_east_window` — temporary position for short east/northeast targets while continuously supervised; keep the tripod behind the sidewalk.
3. `west_past_lamp` — optional outreach position beyond the direct streetlight only on safe private ground with permission; never in the roadway or pedestrian path, and never unattended.

Do not use the western sidewalk position for imaging. The lamp is close enough that a filter cannot solve the direct-flare problem.

The driveway's clearest view is overhead, but Alt-Az sessions should not be centered directly on the zenith. Use the northern/high-northeastern corridor primarily between about 50 and 78 degrees altitude. Near 80–85 degrees, watch the keeper rate and move to the next target rather than forcing the mount through its fastest azimuth motion and strongest field rotation.

Use the exact footprint where the telescope will sit. The phone lens should be close to the telescope's working lens height, roughly 45–55 cm above the ground.

Minimum four-photo set:

- North, centered on 000 degrees
- East, centered on 090 degrees
- South, centered on 180 degrees
- West, centered on 270 degrees

Better eight-photo set: add NE, SE, SW, and NW. Use the phone's normal 1x lens in landscape orientation, keep the horizon near the middle, and overlap neighboring frames by about 25–30%. Do not use panorama mode or digital zoom. Take the whole set without changing position.

Also provide:

- one photo from the scope toward the streetlight;
- the streetlight's approximate compass bearing;
- one photo back toward the scope from the streetlight direction;
- whether the light is above or below the intended telescope lens line;
- one daylight photo showing the ground/tripod footprint.

Avoid including a readable house number, vehicle plate, or unnecessary GPS metadata. Approximate Marietta coordinates are sufficient for the sky model.

From these images, build a horizon mask recording obstruction altitude by azimuth. Targets should normally be scheduled at least 8–10 degrees above the measured obstruction, not merely above the mathematical horizon.

## Streetlight strategy

- Use the house, fence, or a solid existing object to put the telescope in shadow from the lamp while preserving the largest useful sky window.
- Direct line-of-sight shielding matters more than moving a few feet farther away.
- Never wrap or cap the operating telescope, obstruct its moving arm, or attach a large wind-catching panel to the tripod.
- If a freestanding opaque screen is needed, place and secure it separately several feet away and confirm the telescope cannot slew into it.
- Turn off nearby user-controlled exterior lights and indoor lights shining through windows.
- The dual-band filter helps emission nebula contrast, but it does not cure direct glare. Galaxies still need the broadband/UV-IR path.
- At the Dobsonian position, turn off porch, garage, and landscape lights, allow phone night vision to settle, and check both the telephoto and 63-degree wide camera for a flare streak before starting the stack.
- If the streetlight remains directly visible, use a separate, securely anchored opaque panel on the lamp side of the telescope. Size and position it only after verifying the full slew envelope; do not attach it to the telescope or tripod.
- Wide-angle Milky Way/nightscape capture is much more vulnerable to this lamp than narrow telephoto DSO work. Reserve serious wide-angle work for darker travel sites.

## Monday night schedule, weather permitting

The times below are target windows, not a requirement to remain outside all night. A successful first session can be 45–90 minutes. Integration accumulates across separate supervised evenings as long as target, filter, exposure family, and framing are recorded consistently.

Approximate Marietta conditions for September 14:

- sunset: 7:45 p.m. EDT;
- astronomical darkness: about 9:09 p.m.;
- crescent Moon: about 15% illuminated, setting about 9:29 p.m.;
- the early forecast is uncertain and currently ranges from partly to mostly cloudy. Recheck cloud, radar, wind, and dewpoint Monday afternoon.

### 7:30–8:30 p.m. — setup and mechanics

- Put the tripod on firm ground, not a deck.
- Mark leg locations with removable tape/chalk so the position can be repeated.
- Level carefully and confirm a complete slew cannot hit a wall, tree, cable, or screen.
- Connect external power with strain relief and a drip loop.
- Verify lens cleanliness visually; do not clean a new lens unless contamination is actually present.

### 8:30–9:10 p.m. — initialization

- Use Alt-Az mode.
- Run compass/level initialization and allow automatic focus.
- Confirm wide-camera pointing and plate solving.
- Select only high-altitude targets visible through the measured opening.
- Enable individual-frame saving before the first science run if available.

### 9:10–10:30 p.m. — dual-band systems test

Preferred: North America Nebula from approximately 9:10 to 10:30 p.m., moving through the high northeast/northern opening at roughly 65–77 degrees altitude. Heart or Soul Nebula is the later northeast alternate. The Veil passes too close to the zenith for the safest first Alt-Az run.

- Enable the dual-band light-pollution filter.
- Capture 30–45 minutes at 10 seconds for the first test.
- Watch for rejected frames, tree intrusion, direct-light wash, dew, or failed plate solves.
- Do not chase the target if it enters the near-zenith mechanical/tracking region; choose the other Cygnus target or wait.

### 10:30 p.m.–12:15 a.m. — galaxy test

Preferred: M31, climbing through the usable northeast window from roughly 43 degrees at 10:45 p.m. to 60 degrees shortly after midnight. Finish the main run before it approaches 80 degrees around 2 a.m.

- Use broadband/UV-IR, not dual-band.
- Capture 30–60 minutes.
- Use native framing first; save mosaics for a later night.

### 12:15–1:15 a.m. — broadband star-field test

Use the Double Cluster as it climbs through the northeastern opening at roughly 43–52 degrees altitude.

- Continue with broadband/UV-IR and native 1x resolution.
- Capture 30–45 minutes at the default 10 seconds.
- Stop and verify both the device stack and matching individual FITS count.

### Optional late test — M33

M33 is only about 33 degrees high in the east at 11 p.m., about 57 degrees at 1 a.m., and about 70 degrees at 2 a.m. It is faint and should not determine whether first light was successful.

Because the garage blocks the east and M33 passes close to the zenith, its usable Alt-Az window is narrow. Attempt it around 1:15–2:30 a.m. only after GOTO/plate-solving confirms it has cleared the roof, and stop before it moves above roughly 80 degrees. If it remains obstructed, use the Heart or Soul Nebula in the open northeast instead.

If the eastern opening is clear and the system has behaved reliably:

- use broadband;
- try 20-second exposures if the current Alt-Az firmware offers them;
- collect 45–60 minutes as a pipeline sample;
- plan the real project as multiple nights totaling 10–20 hours.

There is no need to wait outside until 2 a.m. on first light. Treat this as a future short-session window after the eastern obstruction is measured from the sidewalk survey.

## Short-session operating plan

Use repeatable 45–90 minute blocks instead of unattended overnight operation:

- **Session A:** setup verification plus 30–45 minutes on North America with dual-band.
- **Session B:** 60–90 minutes on M31 with broadband.
- **Session C:** Double Cluster focus/star-shape test, then Heart or Soul with dual-band.
- **Session D:** M33 only during a verified roof-clearing window; repeat on later nights.
- For an east-rising target hidden at the Dobsonian position, move to `driveway_east_window` for one supervised 30–60 minute block rather than leaving the scope there overnight.

Copy and ingest the FITS files after every session. Multi-night integration is the intended workflow, so ten one-hour supervised sessions can become a ten-hour master without leaving the telescope outside all night.

## Neighbor outreach mode — visible results in 2–15 minutes

The app live stack is the presentation view; simultaneously saved individual FITS are the later processing data. Prepare the telescope and begin the first target before inviting people over so guests immediately see a recognizable image.

### Fast targets for September evenings

- **Moon:** immediate and dramatic when available; no stacking wait. Use the solar-system mode. Never confuse the Moon procedure with solar observing.
- **Albireo or another colored double:** immediate colored stellar pair and a good focus demonstration.
- **M13 globular cluster:** recognizable in roughly 2–5 minutes and increasingly resolved by 10–15 minutes; requires the safe west-past-lamp position during this season.
- **M57 Ring Nebula:** its small ring can appear quickly, with better color after 5–10 minutes; use app display magnification only after capturing at native 1x.
- **M27 Dumbbell Nebula:** strong shape and color in roughly 5–10 minutes when a southern opening is available.
- **North America or Veil:** dual-band; structure should become apparent within 10–15 minutes, though the finished image still benefits from much longer integration.
- **M31:** a bright core appears quickly and dust structure develops with stacking; allow about 10–15 minutes for outreach and hours across nights for the serious version.
- **Double Cluster:** a dense, colorful star field within a few minutes and especially reliable for live demonstration.

Do not choose M33 as the first live demonstration. It has low surface brightness and is a patient multi-session target. Later in the year, M42 Orion becomes the premier rapid neighbor target, with the Pleiades and Rosette as strong companions.

### Suggested 30-minute neighbor program

1. Open with a saved full-resolution image in the app gallery while the telescope initializes.
2. Show the wide camera and Sky Atlas/GOTO so guests understand where the telescope is pointing.
3. Spend 3–5 minutes on a bright cluster, double star, or the Moon.
4. Start a 10–15 minute nebula or galaxy stack and let everyone watch the image improve.
5. Show the frame count/integration clock and explain that the later finished image combines the authentic photons from many short exposures.
6. Save the app result and preserve the individual FITS for SeestarFlow.

Use a tablet or screen-mirrored phone if available so people do not crowd or touch the tripod. Keep the screen dim and red where practical after alignment.

## Sidewalk east/west survey

Take east- and west-facing photographs from the sidewalk/driveway intersection using the same 1x landscape method, plus one photograph looking back toward the intended telescope position. Record whether the streetlight bulb is directly visible and its bearing.

Use the sidewalk only as a camera survey position. Keep the telescope on private driveway pavement, behind the sidewalk and outside the path of pedestrians, vehicles, sprinklers, and curb runoff. If moving the telescope toward the driveway apron materially lowers the roof/tree obstruction, mark a safe repeatable position there and use it only while supervised.

Survey result: the east window is potentially useful; the west position is rejected because the streetlight is directly visible and creates strong flare.

## Second clear night — controlled exposure test

Use one target, framing, filter, focus, and time window. Capture at least 30 frames at each available duration (10, 20, and 30 seconds in Alt-Az; 60 seconds only after successful EQ setup). Compare:

- acceptance rate;
- stellar FWHM and ellipticity;
- background level and gradients;
- saturated pixels;
- signal-to-noise per accepted minute;
- edge rotation/cropping loss.

Choose the exposure with the best usable signal per unit clock time, not the longest setting.

## EQ is a separate commissioning phase

The official procedure requires an EQ wedge/head, the tripod fully extended at its widest stance, one tripod leg toward true north, an open star field, and polar-alignment errors within one degree. Sixty-second exposures are available only in EQ mode. Do not combine first-use troubleshooting with first-time EQ alignment.

Once the required head/plate is present:

1. practice the mechanical conversion in daylight without slewing;
2. confirm clearances and center of gravity;
3. run polar alignment in a sufficiently open part of the yard;
4. test 10/20/30/60 seconds on the same target;
5. retain every frame and compare keeper rate scientifically.

## Data offload and preservation

After each night:

1. Shut down normally so the arm returns home.
2. Connect by USB-C and copy the entire target/session folder to the PC.
3. Ingest the copied session into SeestarFlow; preserve original filenames and SHA-256 hashes.
4. Confirm file counts and hashes before deleting anything from the telescope.
5. Keep the Seestar-generated stack as a reference, but perform our quality filtering and integration from individual FITS frames.
6. Maintain separate folders for each night, filter, exposure length, and mount mode.

Suggested session labels:

- `2026-09-14_backyard_firstlight_broadband_altaz_10s`
- `2026-09-14_backyard_firstlight_dualband_altaz_10s`
- `2026-09-15_backyard_m33_broadband_altaz_20s`

## Stop conditions

Stop and bring the telescope inside for rain, condensation entering openings, thunderstorms, unexpectedly strong wind, unstable footing, cable snagging, or a risk of the arm striking an obstruction. Do not leave the device unattended merely because Plan Mode continues after the phone disconnects.

## Information needed after the horizon photos

- streetlight bearing and whether it is directly visible from the tripod footprint;
- a nighttime check for Polaris, about 34 degrees above true north, to determine whether the site can support EQ alignment;
- confirmation that the photographed position is the final tripod footprint;
- any hours when exterior lights are automatically switched off;
- whether an EQ wedge/head and quick-release plate were included or ordered.

With that information, replace this provisional schedule with an obstruction-aware target calendar and safe slew windows for the backyard.
