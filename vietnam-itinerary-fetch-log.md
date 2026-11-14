---
name: vietnam-itinerary-fetch-log
description: Log of every external data fetch for the vietnam-itinerary site — source, date, result
tags: [log, fetch, vietnam-itinerary]
---

# Fetch Log — Vietnam Itinerary

## 2026 Q4

- [2026-11-14] Q4 | urllib redirect lookup (manual, no tool) | maps.app.goo.gl short links from the public guide (30) | resolved to Google place names, used as planner "Copy address" text. Two links don't match their guide labels: "Nice Bar" opens a place named "Nọt", and "Best café viewpoint" opens a Cộng Cà Phê branch.

- [2026-11-14] Q4 | WebSearch (manual research, no tool) | hotel booking sites and restaurant guides | addresses for the private (encrypted) itinerary. One hotel's house number varies across listings, so check it on the booking confirmation. Venue names stay out of this public log.
- [2026-11-14] Q4 | curl (manual, no tool) | open.er-api.com /v6/latest/EUR + jsdelivr fawazahmed0 currency-api eur.json | EUR→VND changed from 28,985 to 28,400 (rounded; sources 28,411.71 / 28,302.55) → [[fx-eur-vnd-2026-11-14]]
