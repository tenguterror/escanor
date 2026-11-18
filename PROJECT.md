# ESCANOR — Project Plan

**Created:** November 17, 2026  
**Status:** Planning / repository initialization  
**Owner:** Tengu

## Official motto

**Understand the car. Master the drift.** ☀️

## Mission

Build an approachable, local-first drifting coach so drivers can learn from reliable telemetry, understand their car, improve their judged line and proximity, and evaluate changes scientifically.

## Confirmed decisions

- First product: **local web app** for the driver's own PC.
- AI-provider-independent: Claude, ChatGPT/OpenAI, Gemini, and local LLMs are target options.
- Numerical measurement and replay parsing are deterministic; AI interprets results, not fabricates them.
- Support track layout, sections, zones and provenance; teach through data and controlled experiments.
- Start with Assetto Corsa; add **MoTeC i2 telemetry import/export compatibility** as a planned capability.
- Preserve honest uncertainty, driver feel, and **one change at a time** in setup tests.
- Two planned editions: **Escanor Sim** (Assetto Corsa, free and open source) and **Escanor Motorsport** (real-world telemetry, paid product with inspectable/source-available code; precise licensing model pending).
- Real-world edition should support **off-the-shelf motorsport loggers** as well as an optional **Escanor-tested, known-good hardware kit**.
- Explore **track-day hardware rentals** and ongoing maintenance/support revenue, keeping grassroots accessibility central.

## Product and business direction — November 17, 2026

### Escanor Sim — free / open source

- Local Assetto Corsa replay decoding, track and zone analysis, AI-independent exports, coaching, setup experiments.
- Public-source community project; specific approved open-source license to be selected before accepting contributions or distributing code.
- No paywall on essential simulator analysis.

### Escanor Motorsport — paid / source visibility required

- Real-world analysis fed by GNSS, IMU, optional ECU/CAN and third-party motorsport telemetry or MoTeC-compatible exports.
- Potential paid official software distribution, updates, installation and maintenance/support; optional known-good hardware bundles and track-day rentals.
- Open interface/specifications and ability to inspect code are goals; whether the **real-world edition** is fully OSI-open-source or source-available under a commercial license is **undecided**.
- IMPORTANT: an OSI-compliant open-source license permits redistribution, including free redistribution. Charging for copies and services is allowed, but the license cannot ensure that every user pays. A paid-use requirement for the code itself generally entails source-available rather than open-source licensing.
- Investigate clean module boundaries and IP ownership/contributor terms before choosing copyleft, commercial, or dual-licensing approaches. Obtain qualified legal review before commercial launch.
- Keep motor-vehicle analysis post-run, document GNSS/IMU calibration uncertainty, and avoid safety-critical real-time driving instruction.

### Proposed shared engine

```text
Assetto Corsa replay adapter       GNSS / IMU / ECU / logger adapter
              \\                     /
               Common telemetry schema
                       |
       Validated metrics, line and zone analysis
                       |
          Local reports / provider-neutral AI
                       |
       Escanor Sim UI or Motorsport UI
```

## Confirmed requirement — cross-platform support

**Target operating systems:** Windows and Linux first; macOS where supported by the data source and dependencies. Development begins on WSL2 Ubuntu, but the shipped application must not depend on WSL.

- Keep replay parsing, telemetry normalization, track analysis, local web server and dashboard **OS-independent** (Python/portable web technologies).
- Use platform-neutral filesystem paths and configuration: `pathlib`, user-selected replay/log directories and application data directories. Do not hardcode `C:\\Users\\vegas`, `/mnt/c` or a OneDrive path.
- Keep file discovery/watching behind an adapter. Prefer a cross-platform watcher, with an appropriate polling fallback for WSL reading Windows-mounted files and network mounts, where filesystem events may be unreliable.
- Separate **offline replay analysis** from **live telemetry acquisition**. Original Assetto Corsa's Windows shared-memory interface requires a Windows-specific collector; Linux or macOS analysis clients can still work with saved files or a network stream. Validate game availability and supported sources per OS rather than claiming every game runs natively everywhere.
- Include automated tests for supported OS platforms in CI when implementations exist; expose unsupported source integrations clearly instead of breaking the whole app.

**Implementation priority:** Architecture constraint confirmed now; first milestone still decoding and verifying a known-good E46 `.acreplay` in WSL2.

## Proposed architecture — not yet finalized

```text
Local React dashboard (proposed)
          |
FastAPI server on localhost (proposed)
          |
   +------+------------------------+
   |      |                        |
AC replay decoder            Track profiles
   |      |                        |
   +-- Deterministic metrics / zone analysis
                  |
     Versioned run_analysis.json
                  |
     +------------+-------------+
     |                          |
Portable AI export       Provider adapters (later)
(paste into any AI)      OpenAI / Anthropic / Gemini / local
```

Persist session metadata, setup diffs, track profile versions and driver notes locally (SQLite proposed).

### MoTeC i2 track

Investigate ingestion/export of MoTeC-compatible telemetry files and/or CSV exports from i2, with verified units, sampling rates, channel identities, timestamps and alignment to `.acreplay`. Do **not** assume native Assetto Corsa replays contain every channel shown in i2.

## Data contract

- Decoder checks file format/version, frame count, timestamps and continuity, car count, physical ranges and coordinate systems.
- Track profiles store map-to-world transforms, sections, zones, *source*, and revision. Zones are explicitly labeled official/organizer/community/user-defined.
- Metrics have names, units, sampling/derivation descriptions, quality flags, and supporting time/position ranges.
- Versioned `run_analysis.json` is the immutable evidence record passed to AI.
- AI output contains observations, supported hypotheses, drills and **at most one** proposed setup experiment.

## MVP

1. Decode and validate one known-good single-car `.acreplay` file here, using baseline values from independently validated analysis.
2. Specify versioned provider-neutral run report schema and fixtures.
3. Show Bihoku D1 Lights track profile, driven line, sections and clearly attributed zones.
4. Export measured report + AI prompt and save driver feel.
5. Compare repeated runs, preserving one-change test protocol.

## Later

- MoTeC i2 telemetry import and replay synchronization.
- Integrated cloud/local LLM provider adapters and opt-in transmission.
- In-app setup-effect explanations with controlled experiment history.
- VR stutter/frame-time correlation when timestamps can be aligned.
- Multiple cars per replay and tandem lead/chase analysis.
- Track profile editor and community profiles.

## Parking lot — other driving games (deferred, optional)

**Status:** Idea only. Not an MVP requirement. Abandon if maintainability, multiplayer limits, data quality or legal compatibility makes it impractical.

- **Forza Horizon 6:** Official `Data Out` UDP packets provide live player-car telemetry including world position, yaw/orientation, local velocity, driver inputs, tires and engine channels. A future optional logger/adapter could capture runs while driving and map fields into Escanor's versioned common telemetry schema. Native game replay playback does *not* emit this stream, so sessions must be logged live. Official format documentation: https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation
- **CarX Drift Racing Online:** Investigate community-supported data interfaces, e.g., ErinSteph/ErinsMod (Outgauge JSON/binary endpoints) and existing competition-zone judging work such as CHAPPiE. Check available channels, mod reliability, version compatibility, mod policies and multiplayer capture before proposing a supported adapter. https://github.com/ErinSteph/ErinsMod ; https://chappie.online/download
- **Events:** Track profiles and attributed user/event zones are reusable concepts. Before promising tandem analysis, test whether a legally permitted data source supplies synchronized telemetry for **both** vehicles; player-only telemetry cannot measure the other driver's exact line.
- **Architecture decision for now:** Keep the common telemetry schema and source-adapter boundary generic; do **not** implement FH6 or CarX until the Assetto Corsa decoder and track-zone MVP work end-to-end.

## Confirmed direction — Live Mode and LAN coaching

**Goal:** A driver can have Escanor visible on a second monitor while an invited coach watches from a laptop/browser on the same local network. The coach gets real-time run metrics and an automatic, evidence-backed summary **as soon as the run finishes**.

### User experience

- **Driver dashboard (same PC):** current speed, drift angle (when accurately derived), throttle, map position, section/zone indicators and recording status; remain unobtrusive during driving.
- **Coach dashboard (LAN browser):** live track trace, section progression, per-zone measurements and read-only telemetry. No installation required on the coach laptop.
- **Post-run review:** detect or let the driver mark run end; calculate finalized metrics, publish a run summary, show one priority coaching point, and compare with the previous run.
- **Optional later:** coach annotations, session sharing and between-run feedback. No safety-critical real-time commands to a moving driver.

### Proposed implementation (not yet finalized)

- Read Assetto Corsa live physics through the game host's **shared-memory interface**; support offline replay files via a separate adapter.
- Capture high-resolution timestamped samples locally and derive standardized telemetry; stream **downsampled** display updates from a local Python backend to authorized browser clients over WebSockets.
- One web dashboard with **Driver** and **Coach** views, served from the sim PC; access from another device using its LAN IP or local hostname. Keep the app usable without Internet/cloud services.
- Share data only when driver starts a session, with explicit permission, session-specific access token, optional LAN/TLS protection where appropriate, and simple stop/revoke controls. Do not expose raw telemetry to the public Internet by default.
- Handle connection drops, clock synchronization, read-only clients, CPU overhead and buffering so a network or AI failure does not affect sim gameplay.
- AI recommendations happen after a run, based on finalized validated metrics; a coach may inspect live measurements but should not receive unverified diagnoses presented as facts.

**Priority:** Product direction **confirmed**, implementation **after** the single-car replay decoder and track analysis are validated. Stage into local-only live display, LAN viewer, then automated post-run coach report.

## Confirmed direction — Motorsport vehicle-health correlation

**User need:** Real-world drift teams frequently already connect tuning laptops and ECU logging equipment to their cars. After a run, the driver and coach should be able to correlate an unexpected loss of performance at a precise track location with synchronized engine and vehicle sensor channels.

### Potential post-run report

- Playback/overlay: speed, path, yaw and drift angle alongside RPM, pedal position, manifold pressure, fuel pressure, lambda/AFR, ignition/injection status, coolant/oil temperatures and fault codes **when that data is actually logged**.
- Flag measured abnormalities, such as fuel-pressure deviations from the engine's valid target or ECU-reported misfire/fault events. Show which exact sensors and time ranges support the finding.
- Distinguish **measured symptom** (e.g. pressure sag), **plausible hypothesis** (e.g. fuel delivery issue), and **confirmed diagnosis** (only with appropriate evidence and technician confirmation).
- Align all channels by timestamp and track coordinates; record sample rate, missing channels, unit conversion, timestamp drift, logging gaps and sensor/ECU calibration.
- Explain driving implications without blindly attributing a power-loss event to the driver. Compare similar runs to spot repeatable section-linked symptoms.
- **Read-only diagnostics:** Escanor must not automatically change ECU maps, tune ignition/fuel, disable engine protection, or issue vehicle-control commands. Do not replace established safety alerts; advise checking with qualified mechanics/tuners when potentially damaging conditions occur.

### Integration exploration

Prioritize **existing motorsport ECU/data-logger logs** and exports (including MoTeC i2-compatible workflows) rather than requiring the Escanor hardware kit. Capability varies by ECU/logger, enabled channels and sensor installation; future adapters should state exactly what each supported device can provide.

**Status:** Product vision confirmed; adapter support and engine-health analysis are post-MVP research and validation work, not a claim of existing capability.

## Confirmed direction — ECU fuel map / wideband lambda analysis (Motorsport)

**Concept:** After an on-track run, provide read-only, position- and time-aligned visualization of the ECU's operating regions (RPM vs load) against the **correct calibration snapshot**, measured/target lambda, closed-loop corrections, fuel pressure and driver inputs. Help a tuner understand whether inconsistent engine response may have disrupted a drift run.

### Required inputs and interpretation

- Capture **ECU calibration snapshot** with fuel/VE tables, axes, active maps/modes, lambda target, and correction strategies; a datalog alone may *not* contain the table values or which map was active. Keep a calibration identifier/version for every run.
- Capture available logged channels with units, sampling rate and provenance: RPM, MAP/load, throttle, lambda targets and measured wideband lambda (both banks if applicable), lambda control trims, fuel pressure *and manifold pressure*, injector pulsewidth/duty, relevant protection and fault flags, and ignition/boost channels where supported.
- Map time samples to **interpolated** operating regions, not naïvely one fixed cell, and present coverage/dwell and transient conditions. Compensate where validated for sensor lag, log synchronization, dynamic enrichment, closed-loop control, fuel cuts, and sensor validity.
- Overlay track location and driving performance (speed, angle, throttle, changes in acceleration/rotation) to show **correlation**, not automatically assert causation.
- Flag deviations from verified, engine-specific targets and identify *possible* causes for further investigation (e.g. sensor, misfire, fuel system, calibration). Surface confidence and missing data explicitly.
- Deliver a prioritized **review suggestion for a qualified tuner**, never an unverified cell value, instant calibration patch, or automatic ECU write.

### Integration strategy and constraints

- Start with imported/exported logs and tune snapshots from supported existing ECUs; do not need Escanor-branded hardware.
- Investigate MoTeC M1/M1 Tune and i2 workflows, Haltech, Link and other vendor-supported interfaces incrementally, respecting file-format and software license restrictions.
- Preserve read-only design. No commands that alter ECU calibrations, disable failsafes, or apply adjustments during a run.
- **Priority:** Future Motorsport development, not part of initial Assetto Corsa replay MVP. Build after verified telemetry import/time alignment and run-health correlation.

## Parking lot — live event demonstration (future)

**Concept:** SEMA or grassroots track-event booth where visitors drive an Assetto Corsa simulator while Escanor shows a live spectator display of track position, speed, throttle, approximate drift angle and judged-zone proximity. After each run, produce a concise coaching report, offer a second run for comparison, and optionally let a visitor export their own report via QR code.

**Technical exploration:** For original Assetto Corsa, investigate live shared-memory physics, graphics, and static data as a distinct adapter from offline `.acreplay` decoding. The common telemetry schema should support both live streaming and offline post-run analysis.

**Guardrails:** Keep computationally heavy AI analysis and recommendations after the run; don't distract the driver mid-corner. Label zones as official or demonstration-defined, account for geometric/telemetry uncertainty, sanitize public leaderboards, and obtain opt-in before publishing or sharing participant data.

**Priority:** Deferred showcase concept, **not** an MVP dependency. First prove repeatable, validated single-car replay measurements.

## Parking lot — multi-discipline motorsport platform (future vision)

**Idea raised November 17, 2026:** Escanor's underlying telemetry, track-map, run-comparison, vehicle-health and coach-facing analysis could extend beyond drift into endurance/sports-car racing (including Le Mans-style events), drag racing, and SCCA/club racing.

**Status:** Exploratory architecture direction, *not* a promise to build these products or change the Assetto Corsa drifting MVP.

### Architectural principle

**Shared, sport-agnostic evidence engine; discipline-specific scoring and coaching.**

- Keep timestamped telemetry acquisition, units, provenance, quality flags, synchronization, run storage, visualization and optional AI adapters generic.
- Implement per-discipline analysis profiles with explicitly defined metrics, event rules, intervals and failure cases.
- Do not assume a metric carries the same interpretation in all motorsports: large yaw/slip angle is a target in drifting but may be counterproductive on a road course.
- Let a race session define run type: drift judged run, lap, stint, drag pass, test/qualifying. Sports-specific UI can be composed on the common engine rather than forced into one drift-centric dashboard.
- Keep diagnostic outputs read-only and separate mechanical health observations from driver coaching and race strategy.

### Potential discipline modules (unvalidated concepts)

- **Drift (MVP):** car body slip angle, track/clipping zones, initiation, transitions, consistency, lead/chase when validated.
- **Circuit / SCCA club racing:** braking markers, apex/line, exit speed, segment times, tire temperatures (if logged), reproducibility.
- **Endurance / Le Mans-style racing:** stint consistency, fuel use, temperature trends, tire-performance changes and comparisons between drivers where data exists.
- **Drag racing:** launch/60-foot/segment times, wheelspin, acceleration, shift execution, power-delivery or fuel-pressure anomalies when sensors support them.
- Event-specific recommendations must use validated sensor channels, sanctioned rule references where applicable, and explicit limitations. Le Mans-level team capabilities are a distant ambition, not a current product claim.

### Business hypothesis to test later

A reliable, affordable motorsport **data interpreter and coach-facing workflow** could interest grassroots drivers and instructors. Existing professional telemetry and coaching systems make this a competitive market; do not presume unmet demand. Validate usefulness and willingness to pay with users before broadening scope.

### Decision guardrail

**Do not build modules for other disciplines yet.** First validate Assetto Corsa drift replay decoding and track-zone analysis, then prove the same evidence schema can accept another telemetry source. Revisit branding and broader architecture only if real user evidence supports expansion. Retain current motto: *Understand the car. Master the drift.*

## Known constraints / uncertainties

- Existing Escanor instructions describe Assetto Corsa single-car `.acreplay` v16 decoding; an independent executable decoder and test replay are not yet in this repository.
- Brake channel mapping requires independent verification. Replay-derived steering is not guaranteed to equal driver steering input; force-feedback forces are not stored in the replay.
- Official event clipping zones are not inferable from the map image alone.
- AI analysis cannot prove a car-setup cause from a single run.
- No hosted services or user accounts in initial MVP.

## Proposed stack (pending explicit decision)

Python, FastAPI, React, SQLite; Ollama or compatible endpoint for local models.

## Development progress

### November 17, 2026 — Replay header inspector

- Created `inspect_replay.py`, a Python command-line utility.
- Accepts a user-supplied replay file path.
- Reads and displays the first 32 bytes of a replay.
- Decodes the first four bytes as a little-endian version number.
- Confirmed version 16 using a local E46 Bihoku replay.
- Tested missing arguments, nonexistent files, and incomplete headers.
- All four manual tests passed.

**Status:** Header inspection working. Full replay decoding and
telemetry extraction are not yet implemented or validated.

## Next action

**Validate replay decoding** against one uploaded, known-good E46 `.acreplay`; retain it locally as a private test fixture and record independently verified expected measurements. Do not publish the raw replay without permission.

## Open decisions

- Choose open-source license for Sim, and determine whether Motorsport is true open-source with paid services or source-available with a paid-use license (and whether dual licensing is appropriate).
- Final frontend/backend/database selection.
- Track profile format and zone-review process.
- MoTeC i2 input formats and supported data acquisition workflows.
- Golden replay fixture and agreed metrics.
