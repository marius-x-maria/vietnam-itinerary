---
name: vietnam-itinerary-agent
description: Agent briefing for the Vietnam Itinerary site — role, current state, capability registry, rules
tags: [agent, briefing, vietnam-itinerary]
---

# Agent Briefing — Vietnam Itinerary

## Your Role

A Tier-0 static site under [[vibe_coder]] — the shared, public travel guide for the Onofrei and
Miron families' November 2026 Vietnam trip. One page, no build step, no backend.

## How to Operate

- `index.html` is the whole site. Edit it directly; there is no build step.
- Source of truth for raw content is a shared Google Doc the families edit — this site is the
  polished published view, not a live sync. Re-copy/re-polish after real Doc changes.
- Keep the Romanian-default / English-toggle `data-i18n` pattern when adding new copy: wrap
  translatable text in `<span data-i18n="key">Romanian text</span>` and add the English string to
  the `dict.en` object in the inline `<script>` at the end of the file. Proper nouns (hotel/place/
  restaurant names, family surnames) are never translated.
- Links are organized per destination (Hà Nội / Sa Pa / Phú Quốc) under Hotels / Places to
  Visit / Restaurants, grouped by category. A `.row` is a primary link; a `.pin-link` is a
  secondary map link alongside it.

## Current System State

### Branches
main ← stable, pushed to `origin/main` (public: `github.com/marius-x-maria/vietnam-itinerary`),
served via GitHub Pages from root.

### What's Built

| Component | Status |
|---|---|
| Hero + route diagram (two families converging on Phú Quốc) | ✅ Complete |
| Family itineraries (confirmed flights, open days) | ✅ Complete |
| Prep: documents, essential apps (with App Store/Google Play links), exchange rate, food-poisoning note | ✅ Complete |
| Destination guides: Hà Nội, Sa Pa, Phú Quốc (hotels, places, restaurants) | ✅ Complete |
| Romanian default / English toggle | ✅ Complete |

## Capability Registry

| Capability | State | Note |
|---|---|---|
| Static bilingual guide (RO/EN) | `included` | Toggle persists per-browser via `localStorage` |
| Destination hotel/place/restaurant links | `included` | Sourced from the shared Google Doc |
| Family itineraries with open-day markers | `included` | Specific days intentionally left open — see the source Doc |
| Live sync with the Google Doc | `absent` | Manual re-publish, not automated |
| Embedded maps | `absent` | Links open externally (Google Maps / Klook / etc.) |
| Build tooling | `removed` | Deliberately zero-build Tier 0 — matches `wedding`/`electronics-website` |
| Automated tests | `absent` | No test need for a static content page |

## Known Trade-off (flagged to Marius, accepted)

This page is **public** and names both families by surname with exact travel dates — a minor
physical-security consideration (signals when both households are away). Marius explicitly chose
to proceed as-is rather than anonymize or keep it private. If that changes, redact surnames to
"Family 1"/"Family 2" in `index.html` and keep real names only in the private Google Doc / the
`itinerary-app` project.

## Rules

- Never commit `.env` or credentials (none expected on this project).
- Re-run [[security_checker]] before any future push, same as every other repo.
