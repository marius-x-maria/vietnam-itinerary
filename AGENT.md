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
  both family timelines encrypted behind one family code). Edit directly; the only build step is `tools/encrypt_private.py`.
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
| Embedded maps | `included` | Only the private activity map on `itinerary.html`; the guide page still links out |
| Build tooling | `removed` | Deliberately zero-build Tier 0 — matches `wedding`/`electronics-website` |
| Encrypted private itinerary | `included` | `tools/encrypt_private.py` + unlock form in `itinerary.html` |
| Per-family day planner | `included` | Inside the encrypted block. Switch "Pentru: Familia O · Familia M · Ambele": each family has its own free days (`days.o` / `days.m`, a day can set a per-slot city `sc` for travel days); "Ambele" shows only shared days/slots, saves only the slots changed there to both families and flags slots where O and M differ. Both timelines are rendered by JS from `o-fixed` JSON (`fam.o` / `fam.m`: bookings, nights, map days) merged with that family's saved plan. Calendar id `31` = 1 Dec (shown via `dn`). Planner = a date dropdown (◀ ▶, labels show city, planned count, unsaved) showing one free day at a time (Excursion / Lunch / Dinner / Bar-coffee, + Tailor on Hà Nội days), each with an editable time; "Save day" applies it to the timeline; plan in `localStorage` (`vn-plan` = `{o, m}`; the older `vn-plan-o` is still read once), shared via `#plan=` link (`{p: O, m: M, c}`; older bare-array and `{p, c}` links load into Family O) (URL fragment, never sent to a server). Planner JS is generic in `itinerary.html`; all data lives in the fragment |
| Activity map | `included` | Inside the encrypted block. Family O / M switch (follows the planner family) picks whose day route, stays and planned pins are shown. Leaflet 1.9.4 (cdnjs) + OpenFreeMap "liberty" vector tiles via MapLibre GL 5.6.0 (cdnjs) and @maplibre/maplibre-gl-leaflet 0.1.3 (jsdelivr), all with SRI; free, no key, no sign-up. Falls back to softened OpenStreetMap raster tiles (`.is-raster`) if WebGL or MapLibre fails. Loaded only after unlock. Filter = one category chip (Toate / Mâncare / Mic dejun & cafea / Bar / Excursii / Croitor) then sub-chips with counts (food kind, café/bar style from `st` + `subTags` in the builder, excursion length); stays and bookings always show as reference points. "Only planned" switch. Pin coordinates come from the guide's Google Maps links (COORDS in the private builder); hotel pins come from OpenStreetMap |
| Itinerary page layout | `included` | After unlock: sticky tabs Itinerariu / Planificator / Hartă (`vn-view`); planner and map panels are moved out of the decrypted fragment into `#view-plan` / `#view-map`; the map is built on first visit to its tab. Icon colours by type (flight sky, hotel plum, food gold, excursion jade, bar plum, tailor lacquer). Buttons are icon-only on phones. In "today" mode during 15–30 Nov, today is highlighted and earlier days fold (`?today=YYYY-MM-DD` to test) |
| Map day route | `included` | "Traseul zilei" select: numbered stops (morning hotel → bookings + planned items → night hotel) with a dashed line, a stop list and a Google Maps directions link (`/maps/dir/?api=1`, coordinates only) |
| Custom places ("Locurile mele") | `included` | "➕ Adaugă alt loc…" in every planner dropdown opens a form: name, Google Maps link (pin read from long links: `!3d/!4d`, `@lat,lng`, `?q=lat,lng`), Klook link, type, Grab address, or a tap-to-place mini map. Saved in `localStorage` (`vn-custom-o`), ids ≥ 1000. The share link (UTF-8 base64 `{p, c}`) carries them. Links are restricted to http(s) and coordinates to Vietnam's bounds; all text goes in via `textContent` |
| Place ratings | `included` | Every place shows "4.6★ (2.700) · description" (Google figures via Wanderlog etc.; tours show "Klook 4.9★ (16)"). Researched picks: [[restaurant-picks-2026-11-15]]; the guide's own places: [[catalogue-ratings-2026-11-15]] (`RATINGS` in the builder). Unverified places and tours that could not be matched to the exact activity get no rating |
| Traditional Vietnamese picks category | `included` | 🇻🇳 "Traditional Vietnamese · Claude's pick", 5 Hà Nội Michelin places (food ids 128-132); Phở Hà Đông id 127 removed. Phú Quốc rows 133-136 researched, not shown: [[traditional-vietnamese-picks-2026-11-15]] |
| Phú Quốc coastal palette + lotus mark | `included` | Sand / sea-teal `--brand` / coral (lacquer token) / palm (jade token). `--brand` is a semantic token; jade keeps its meaning for Hà Nội and excursions. Lotus mark kept |
| Planner breakfast/brunch slot | `included` | Slot shows only `st=brunch` items plus items with `br=1` (ids 111/112) and custom cafés |
| First-visit guide card | `included` | `<dialog id="guide">` in `itinerary.html` (public, generic text): 4 points (Itinerariu / Planificator / Hartă / Trimite planul, ⭐ = Marius's own places, 🇻🇳 = Claude's picks). Opens once per device after unlock (`vn-guide-seen`), "?" button in the view tabs reopens it |
| Marius's own places starred | `included` | Builder prefixes "⭐ " to catalogue names with id < 100; Michelin labels on Claude's picks read "Michelin …" (no ⭐) |
| Automated tests | `absent` | No test need for a static content page |

## Private Data Decision (2026-11-14, Marius chose option A)

- Surnames are replaced by "Familia O" / "Familia M" on the page. Older git history still holds
  the full names and the earlier public Family M timeline; accepted, not rewritten.
- Hotel names, addresses, check-in times, domestic flight times and reservations are **sensitive**
  (they show where a family sleeps each night). They are never in clear text in a served file.
- Clear-text source: `private/family-o.local.html` (git-ignored). `tools/encrypt_private.py`
  encrypts it (PBKDF2-SHA256 300k → AES-256-GCM) into the `PRIVATE_O` block of `itinerary.html`.
  The key is `FAMILY_O_CODE` in `.env`: 16 random chars (~79 bits). Shared with the family by
  private message only. The page decrypts it with Web Crypto and remembers the code per device.
- To change the private itinerary: edit `private/build_fragment.py` (also git-ignored; holds the
  Family O timeline plus the planner data: catalogue of guide places, free days, slots, defaults) → `python private/build_fragment.py
  private/family-o.local.html` → `python tools/encrypt_private.py`, which verifies the round
  trip and that no private term is left in clear text (exit 2 if it is).
- Strength = code entropy only. Never replace it with a short or guessable code.

## In Progress

- None. All shipped and pushed 2026-11-15 (HEAD `271bb7c`). Trip runs 15-30 Nov: fixes only, each with a security scan. Open cosmetic items: 🇻🇳 renders as "VN" on Windows; Hartă icon glyph. Details in `private/NEXT.md`.
- **Pushed 2026-11-15 (`271bb7c`, security Run 043):** (1) Literata never loaded: the Google Fonts request asked for `opsz 18..144`, the font has `7..72`, so every heading fell back to Georgia and "Phú Quốc" showed a detached accent. Fixed in both pages, headings `line-height:1.15`. (2) `itinerary.html`: all labels under 12 px raised to 12 px; map colours are `--map-*` tokens that do not flip in dark (numbered pins were white on light teal in dark). (3) Desktop hero: lower route labels clear the dashed line. Probe on the public view: 0 errors, 0 warnings. **The unlocked view is still not probed or seen**: using the family code from `.env` was blocked by the permission system. Remaining raw hex: route line colour in JS (`itinerary.html`, `L.polyline`).
- **Pushed 2026-11-15 (`60d7b4d`, security Run 042):** accessibility fix found by `tools/layout_probe.py`. Light-theme `--lacquer`, `--jade`, `--gold` darkened to reach WCAG AA on their soft backgrounds (both pages); hero route labels 12 px on phones; `.subhead` and apps toggle 12 px; app-card links 24 px tall. Probe: 0 errors, 0 warnings at 375 and 1280, light and dark, on the public view of both pages. The unlocked (encrypted) view of `itinerary.html` was not probed: it still has 11.5 px labels and raw-hex map pins using the old colours. Fix those at the next re-encrypt.

## Rules

- Never commit `.env` or credentials (none expected on this project).
- Re-run [[security-checker]] before any future push, same as every other repo.
