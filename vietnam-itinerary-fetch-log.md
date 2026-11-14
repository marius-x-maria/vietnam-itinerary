---
name: vietnam-itinerary-fetch-log
description: Log of every external data fetch for the vietnam-itinerary site — source, date, result
tags: [log, fetch, vietnam-itinerary]
---

# Fetch Log — Vietnam Itinerary

## 2026 Q4

- [2026-11-14] Q4 | urllib (manual, no tool) | eng.nhuttailor.vn store list | the guide's tailor map link opens their Ho Chi Minh City store. Their site lists a Hà Nội branch at 20 Tràng Tiền, Hoàn Kiếm, which the planner now uses.
- [2026-11-14] Q4 | urllib (manual, no tool) | nominatim.openstreetmap.org search + reverse (generic User-Agent, ~10 requests, 1.2 s apart) | coordinates for the private map pins, street addresses for two cafés/bars, and a pin for the Hà Nội tailor branch. The Phú Quốc villa pin is approximate (resort entrance).
- [2026-11-14] Q4 | urllib redirect lookup (manual, no tool) | maps.app.goo.gl guide links (31) | exact pin coordinates (!3d/!4d) for the activity map.

- [2026-11-14] Q4 | urllib redirect lookup (manual, no tool) | maps.app.goo.gl short links from the public guide (30) | resolved to Google place names, used as planner "Copy address" text. Two links don't match their guide labels: "Nice Bar" opens a place named "Nọt", and "Best café viewpoint" opens a Cộng Cà Phê branch.

- [2026-11-14] Q4 | WebSearch (manual research, no tool) | hotel booking sites and restaurant guides | addresses for the private (encrypted) itinerary. One hotel's house number varies across listings, so check it on the booking confirmation. Venue names stay out of this public log.
- [2026-11-14] Q4 | curl (manual, no tool) | open.er-api.com /v6/latest/EUR + jsdelivr fawazahmed0 currency-api eur.json | EUR→VND changed from 28,985 to 28,400 (rounded; sources 28,411.71 / 28,302.55) → [[fx-eur-vnd-2026-11-14]]
