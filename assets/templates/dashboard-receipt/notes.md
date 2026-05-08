# Dashboard Receipt Template Notes

A receipt/thermal-printer style dashboard. The entire layout sits on a white "receipt" strip with zigzag torn edges top and bottom, on a black background. Contains a glitchy "SYSOP" logo with horizontal line cutouts, data tables (Core Vitals), dot-fill progress bars (Resource Matrix), SVG signal waveform chart, black-and-white heatmap grid, and event log table. All in Courier monospace.

It implements a `gifted-data-viz` pattern: structured data presented as a stylized, tangible artifact — like a receipt from a cyberpunk server room.

## Reference Use

Treat as reference. Hermes may change the data to personal stats, relationship metrics, weekly reviews, or any structured data. The core idea: make data feel like a physical artifact you can hold.

## What To Change Per Use

- document.title
- Logo/header text
- Vitals data labels and values
- Resource bar labels and fill levels
- Waveform chart data
- Heatmap grid data
- Event log entries
- Receipt width

## What Not To Copy Blindly

- the exact "SYSOP" branding
- the specific system/protocol terminology
- the exact data values

## Best Fit

- tech/programmer themed gifts ("your year in code")
- personal stats dashboards
- analytical "year in review" gifts
- hacker/cyberpunk aesthetic presents
- structured weekly/monthly summaries for data-minded users

## Watch Outs

- Courier monospace is hard to read at small sizes
- receipt metaphor may feel cold without warm content
- zigzag edges use CSS clip-path — test browser support
- heatmap cells are tiny — don't encode critical info there
- purely static — no interaction, works best as a visual statement
- do not use @latest or unstable external dependencies

## Delivery Note

Single HTML file. Google Fonts CDN is acceptable.
