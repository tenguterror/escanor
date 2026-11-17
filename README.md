# Escanor ☀️

**A local-first, AI-independent drift telemetry and coaching project.**

Escanor aims to help Assetto Corsa drivers understand what their car is doing, improve judged runs, and test setup changes against real telemetry—not guesses.

> **Project status: planning / early development.** The GitHub repository is being initialized. A replay decoder has been used successfully in a separate workflow, but its implementation and golden test fixtures have not yet been imported or independently validated here.

## Principles

- **Measure first.** Replay decoding, track geometry, and telemetry metrics are computed deterministically, without an LLM.
- **AI is optional and replaceable.** Export a provider-neutral report for Claude, ChatGPT, Gemini, or a local LLM. Later add API integrations.
- **Explain, don't prescribe.** Coaching distinguishes measured observations, plausible hypotheses, and conclusions supported by repeated tests.
- **Change one thing at a time.** Log setup changes and compare repeatable runs.
- **Local by default.** Replay files, setups, and history stay on the driver's PC unless the driver explicitly exports or shares them.

## Planned first version

1. Import and validate a **single-car Assetto Corsa** `.acreplay`.
2. Load a reviewed **track profile** with layout, course sections, and provenance-tagged clipping zones.
3. Overlay the driven line and report measurements with units and quality flags.
4. Export a versioned `run_analysis.json` and portable coaching prompt.
5. Record driver feedback and compare runs.

**MoTeC i2 integration is planned.** Evaluate imported/exported telemetry logs, channel mappings, timestamps, and alignment to replay data before relying on cross-source comparisons.

## Proposed stack (not final)

- Python engine / FastAPI local backend
- React dashboard
- SQLite run history
- Export-first AI workflow; optional Anthropic, OpenAI, Gemini, and Ollama adapters later

See [PROJECT.md](PROJECT.md) for decisions, architecture, milestones, and open questions.

## Safety and data integrity

Do not commit private replays, personal log files, API keys, or downloaded car/track assets without redistribution permission. Official judging zones must come from documented organizer data, not assumptions derived from track artwork.

## Contributing

Contributions are welcome as the project takes shape. A license and contribution guidelines have **not yet been selected**; until then, public visibility alone does not grant permission to reuse the source code.
