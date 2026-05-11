# Changelog

All notable changes to `dear` are documented here.

This file follows a lightweight changelog style: concise, human-readable, and focused on user-visible capability changes.

## [1.0.0] - 2026-04-10

First public release of `dear` as a relationship-aware gift skill for Claude Code.

### Added

- a complete five-stage gift pipeline: editorial judgment, synthesis, creative concept, visual strategy, and final rendering
- three practical output formats: `h5`, `image`, and `text`, plus `hybrid` mode for format selection by fit
- user-triggered creative and template workflows for turning recipient context into a finished gift
- anti-repetition controls for recent gifts across format, visual style, content direction, concept family, theme, and related metadata
- first-gift strategy that requires real return, not just a recap of the user's setup answers
- image-generation support with provider detection for `OPENROUTER_API_KEY`, `GEMINI_API_KEY`, and `GOOGLE_API_KEY`
- H5 rendering support with reusable templates, audio hooks, asset generation guidance, and browser-based self-check expectations
- onboarding support for taste questions, optional portrait / OC setup, and lightweight image-capability reminders
- public-facing project docs including bilingual README examples, `CONTRIBUTING.md`, and this changelog

### Changed

- the public docs now present the skill as an emotional-value gift engine rather than a generic utility workflow
- format-selection, delivery, and rendering rules now distinguish more clearly between `h5`, `image`, and `text` gifts
- H5 visualization rules now require higher-fidelity handling of characters, objects, and scenes, including image-first or hybrid composition when code-only drawing would look weak
- image rendering guidance now preserves recurring character identity, POV, and workspace-stable output paths more explicitly
- external service dependencies and optional environment variables are documented more clearly in the README

### Removed

- comic-specific workflow, docs, config, examples, and runtime paths from the public release
- motion-generation workflow, provider config, schemas, and runtime paths from the public release

### Known Limitations

- image generation depends on a supported external image API being available
- H5 hosted delivery defaults to `surge.sh`, though the hosting layer is replaceable
- some reference- or concept-only pattern cards do not yet have reusable HTML templates
