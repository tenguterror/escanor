# ESCANOR — Project Plan

**Created:** November 17, 2026  
**Status:** Planning / repository initialization  
**Owner:** Tengu

## Mission

Build an approachable, local-first drifting coach so drivers can learn from reliable telemetry, understand their car, improve their judged line and proximity, and evaluate changes scientifically.

## Confirmed decisions

- First product: **local web app** for the driver's own PC.
- AI-provider-independent: Claude, ChatGPT/OpenAI, Gemini, and local LLMs are target options.
- Numerical measurement and replay parsing are deterministic; AI interprets results, not fabricates them.
- Support track layout, sections, zones and provenance; teach through data and controlled experiments.
- Start with Assetto Corsa; add **MoTeC i2 telemetry import/export compatibility** as a planned capability.
- Preserve honest uncertainty, driver feel, and **one change at a time** in setup tests.

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

- License before inviting contributors or distributing code.
- Final frontend/backend/database selection.
- Track profile format and zone-review process.
- MoTeC i2 input formats and supported data acquisition workflows.
- Golden replay fixture and agreed metrics.
