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

## Known constraints / uncertainties

- Existing Escanor instructions describe Assetto Corsa single-car `.acreplay` v16 decoding; an independent executable decoder and test replay are not yet in this repository.
- Brake channel mapping requires independent verification. Replay-derived steering is not guaranteed to equal driver steering input; force-feedback forces are not stored in the replay.
- Official event clipping zones are not inferable from the map image alone.
- AI analysis cannot prove a car-setup cause from a single run.
- No hosted services or user accounts in initial MVP.

## Proposed stack (pending explicit decision)

Python, FastAPI, React, SQLite; Ollama or compatible endpoint for local models.

## Next action

**Validate replay decoding** against one uploaded, known-good E46 `.acreplay`; retain it locally as a private test fixture and record independently verified expected measurements. Do not publish the raw replay without permission.

## Open decisions

- Choose open-source license for Sim, and determine whether Motorsport is true open-source with paid services or source-available with a paid-use license (and whether dual licensing is appropriate).
- Final frontend/backend/database selection.
- Track profile format and zone-review process.
- MoTeC i2 input formats and supported data acquisition workflows.
- Golden replay fixture and agreed metrics.
