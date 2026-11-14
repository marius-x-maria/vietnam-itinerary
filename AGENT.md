---
name: vietnam-itinerary-agent
description: Agent briefing for the Vietnam Itinerary site — role, current state, capability registry, rules
tags: [agent, briefing, vietnam-itinerary]
---

# Agent Briefing — Vietnam Itinerary

## Your Role

A Tier-0 static site under [[vibe-coder]] — the shared, public travel guide for two families' (O and M) November 2026 Vietnam trip.
One page, no backend; one encryption step for private details (below).

## How to Operate

- Two pages: `index.html` (guide) and `itinerary.html` (family itineraries, family switch,
  encrypted Family O timeline). Edit directly; the only build step is `tools/encrypt_private.py`.
- `itinerary.html` uses `.ro`/`.en` spans (CSS hides the other language) instead of the
  `data-i18n` dictionary; both pages share the `vn-lang` localStorage key. Design tokens are
  duplicated in both `<style>` blocks — change both.
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
| Encrypted private itinerary | `included` | `tools/encrypt_private.py` + unlock form in `itinerary.html` |
| Automated tests | `absent` | No test need for a static content page |

## Private Data Decision (2026-11-14, Marius chose option A)

- Surnames are replaced by "Familia O" / "Familia M" on the page. Older git history still holds
  the full names; accepted, not rewritten.
- Hotel names, addresses, check-in times, domestic flight times and reservations are **sensitive**
  (they show where a family sleeps each night). They are never in clear text in a served file.
- Clear-text source: `private/family-o.local.html` (git-ignored). `tools/encrypt_private.py`
  encrypts it (PBKDF2-SHA256 300k → AES-256-GCM) into the `PRIVATE_O` block of `itinerary.html`.
  The key is `FAMILY_O_CODE` in `.env`: 16 random chars (~79 bits). Shared with the family by
  private message only. The page decrypts it with Web Crypto and remembers the code per device.
- To change the private itinerary: edit `private/build_fragment.py` (also git-ignored; holds the
  Family O timeline plus the "ideas for free days" plan) → `python private/build_fragment.py o
  private/family-o.local.html` → `python tools/encrypt_private.py`, which verifies the round
  trip and that no private term is left in clear text (exit 2 if it is).
- Strength = code entropy only. Never replace it with a short or guessable code.

## Rules

- Never commit `.env` or credentials (none expected on this project).
- Re-run [[security-checker]] before any future push, same as every other repo.
