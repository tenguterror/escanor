# ESCANOR — Project Plan

**Created:** November 17, 2026  
**Status:** Early development: replay header parser (rewrite in progress)  
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

Long-term vision, editions, business ideas and parking-lot features: see **[VISION.md](VISION.md)**.

## Focus rule

Only work that moves the **MVP** forward belongs in this file. New ideas go to VISION.md first.

## Platform constraint (short version)

Windows and Linux first. Development happens on WSL2, but the app must not depend on WSL. Use `pathlib` and user-selected directories; never hardcode paths like `C:\Users\vegas` or `/mnt/c`. Full details are in VISION.md.

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

## Golden test replay

The known-good replay every parsing step is checked against. **Private: never committed** (`data/private/` and `*.acreplay` are git-ignored).

| Field | Value |
|---|---|
| Local path | `data/private/e46_bihoku_golden.acreplay` |
| Original | AC replay `temp` folder, `AC_171126-193711_..._bmw_e46_..._bihoku_highland...acreplay` |
| Size | 31 MB |
| SHA-256 | `3d6b3fa096e47f5ff5c2ca26f848d062b2c5cb09986a9db90993822fec5b5234` |
| Copied / verified | November 18, 2026. Tengu's `sha256sum` of original and copy matched |
| Known values | version 16; weather name length 23; weather `sol_03_scattered_clouds` |

Verify before trusting results: `sha256sum data/private/e46_bihoku_golden.acreplay` must print the hash above. If it doesn't, the fixture has changed and every "known value" is suspect.

## Known constraints / uncertainties

- Existing Escanor instructions describe Assetto Corsa single-car `.acreplay` v16 decoding; an independent executable decoder and test replay are not yet in this repository.
- Brake channel mapping requires independent verification. Replay-derived steering is not guaranteed to equal driver steering input; force-feedback forces are not stored in the replay.
- Official event clipping zones are not inferable from the map image alone.
- AI analysis cannot prove a car-setup cause from a single run.
- No hosted services or user accounts in initial MVP.

## Proposed stack (pending explicit decision)

Python, FastAPI, React, SQLite; Ollama or compatible endpoint for local models.

## Development progress

### Current state

| Component | Status |
|---|---|
| `inspect_replay.py` | Rewrite in progress: step 1 done (reads and decodes the version); v1 is in git history |
| Common telemetry schema | Not started |
| Track profiles | Not started |
| Web app | Not started |

### November 17, 2026 — Replay header inspector

- Created `inspect_replay.py`, a Python command-line utility.
- Accepts a user-supplied replay file path.
- Reads the first 52 bytes of a replay and prints them as hex.
- Decodes bytes 0–3 as a little-endian version number (confirmed 16 on a local E46 Bihoku replay).
- Skips bytes 4–11 (meaning not yet documented).
- Decodes a length-prefixed weather preset string, then a length-prefixed track name string.
- Tested missing arguments, nonexistent files, and incomplete headers.
- All four manual tests passed.

**Status:** Header inspection working on the known replay. Full replay decoding and
telemetry extraction are not yet implemented or validated.

### November 18, 2026 — Code review of `inspect_replay.py` (Baus / Claude, branch `claude`)

Tested with synthetic files only; the real E46 replay was **not** available to the reviewer.

**Bugs (confirmed with synthetic files):**

1. **Silent truncation.** The script reads a fixed 52 bytes, but the weather and track strings are variable length. With a 32-character weather name, the track name came out as an **empty string with no error**. It works on the E46 replay only because those strings happen to be short. Wrong output with no error is the worst kind of failure for a "measure first" project.
2. **Crash on bad bytes.** A non-UTF-8 string (corrupt file, or a file that isn't a replay) raises a raw `UnicodeDecodeError` traceback instead of a clear error.

**Risks / gaps:**

3. **No sanity checks on lengths.** A garbage length value (e.g. 4 billion) is trusted as-is. Real binary parsers check that a length is reasonable *and* that enough bytes actually exist before slicing.
4. **Version is printed, not checked.** The parser assumes the v16 layout but would happily parse a v15 or v17 file with the same offsets.
5. **Mystery bytes 4–11.** Undocumented skipped bytes in a binary format are a future bug. Identify them or note them as unknown in a format spec.
6. **All top-level script code.** Nothing can be imported or unit tested. Fine for a first spike; it becomes the bottleneck as soon as there's a second field to parse.

**Docs drift:** This log previously said "first 32 bytes" while the code read 52 and also parsed weather/track. Keep the log in sync with each commit.

### November 18, 2026 — Rewrite step 1 done (PR #3)

- Tengu deleted v1 and rewrote `inspect_replay.py` from scratch on `feature/inspector-step-1`.
- Opens the replay in binary mode, reads exactly 4 bytes, and decodes them as a little-endian integer.
- Verified on the real E46 Bihoku replay (Tengu's local run): `xxd` shows `10 00 00 00`, and the script prints `Version: 16`.
- Experiment: decoding the same bytes as big-endian gives 268,435,456 **with no error**. This is the reason step 4 must reject any version other than 16.
- Reviewed by Baus on PR #3 and merged into `main` by Tengu.
- Follow-ups from the review: hardcoded personal path (handled in step 4), missing final newline, rename `header` → `version_bytes`.
- Observed in the real replay: bytes 4–11 are `00 00 00 00 00 00 2e 40`; bytes 12–15 are `17 00 00 00`, followed by the weather text `sol_03_scattered...`. Not yet decoded; inputs for steps 2 and 5.

## Replay inspector rewrite plan

Tengu is rewriting `inspect_replay.py` from scratch to learn binary parsing properly. Baus reviews; Tengu writes the code. One step at a time; each step must run before the next starts.

The v1 file stays in git history (commit `08e6c1d`) as a reference. It does not need to be kept in the working tree.

| Step | Goal | Done when |
|---|---|---|
| 1 ✅ | Open a replay in binary mode and print the version number | Prints `16` for the E46 replay (done Nov 18, PR #3) |
| 2 | Read the weather string by its real length, not a fixed window | Works on a synthetic file with a 32+ character weather name |
| 3 | Move "read a length-prefixed string" into one reusable function; use it for weather and track | Both strings come from the same function |
| 4 | Fail loudly: short reads, unreasonable lengths, non-UTF-8 bytes, version ≠ 16. Take the replay path as a command-line argument instead of hardcoding it | Each case prints a clear error and exits non-zero; no tracebacks; no personal paths in the code |
| 5 | Identify bytes 4–11 | Documented in a format notes file, or marked "unknown" with evidence |
| 6 | Automated tests (pytest) using synthetic replay files | Tests cover every bug from the review |

**Current step:** 2

**Milestone — the Catalina Wine Mixer 🍷:** the day Escanor decodes a full Bihoku run end to end. Biggest event of the year.

## Team workflow

- `main` — Tengu's branch; source of truth.
- `claude` — Baus (Claude) updates `PROJECT.md` here: reviews, decisions, progress log. Tengu reviews and merges into `main`.
- Tengu writes the Python. Reviewer branches change documentation only unless Tengu explicitly asks for code.

## Next action

**Rewrite step 2:** read the weather string by its real length. Read the 4-byte length at offset 12, then read exactly that many bytes and decode them as text. Prove it on the real E46 replay, then on a synthetic file with a 32+ character weather name.

Then continue the rewrite plan, and afterwards **validate replay decoding** against the known-good E46 `.acreplay`. Keep it locally as a private test fixture, record independently verified expected measurements, and do not publish the raw replay without permission.

## Open decisions

- Choose open-source license for Sim, and determine whether Motorsport is true open-source with paid services or source-available with a paid-use license (and whether dual licensing is appropriate).
- Final frontend/backend/database selection.
- Track profile format and zone-review process.
- MoTeC i2 input formats and supported data acquisition workflows.
- Golden replay fixture and agreed metrics.
