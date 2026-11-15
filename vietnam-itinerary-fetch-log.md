---
name: vietnam-itinerary-fetch-log
description: Log of every external data fetch for the vietnam-itinerary site — source, date, result
tags: [log, fetch, vietnam-itinerary]
---

# Fetch Log — Vietnam Itinerary

## 2026 Q4

- [2026-11-15] Q4 | research subagents (WebSearch/WebFetch, manual) + nominatim.openstreetmap.org (2 lookups, no pins) | Wanderlog and Spinach Guide Google-rating quotes, Klook activity snippets | ratings for 41 original guide places (8 unverified, 1 skipped), Rico address confirmed as 7 Nguyen Gia Thieu, one Phu Quoc steakhouse qualifies -> [[catalogue-ratings-2026-11-15]]

- [2026-11-15] Q4 | research subagent (WebSearch/WebFetch, manual) + nominatim.openstreetmap.org (~32 lookups) | Michelin Guide pages, Wanderlog Google-rating quotes | 28 places found, 27 added to the planner catalogue, 22 with pins → [[restaurant-picks-2026-11-15]]. CARTO map tiles now need an API key, so the map stays on OpenStreetMap tiles.

- [2026-11-14] Q4 | urllib (manual, no tool) | eng.nhuttailor.vn store list | the guide's tailor map link opens their Ho Chi Minh City store. Their site lists a Hà Nội branch at 20 Tràng Tiền, Hoàn Kiếm, which the planner now uses.
- [2026-11-14] Q4 | urllib (manual, no tool) | nominatim.openstreetmap.org search + reverse (generic User-Agent, ~10 requests, 1.2 s apart) | coordinates for the private map pins, street addresses for two cafés/bars, and a pin for the Hà Nội tailor branch. The Phú Quốc villa pin is approximate (resort entrance).
- [2026-11-14] Q4 | urllib redirect lookup (manual, no tool) | maps.app.goo.gl guide links (31) | exact pin coordinates (!3d/!4d) for the activity map.

- [2026-11-14] Q4 | urllib redirect lookup (manual, no tool) | maps.app.goo.gl short links from the public guide (30) | resolved to Google place names, used as planner "Copy address" text. Two links don't match their guide labels: "Nice Bar" opens a place named "Nọt", and "Best café viewpoint" opens a Cộng Cà Phê branch.

- [2026-11-14] Q4 | WebSearch (manual research, no tool) | hotel booking sites and restaurant guides | addresses for the private (encrypted) itinerary. One hotel's house number varies across listings, so check it on the booking confirmation. Venue names stay out of this public log.
- [2026-11-14] Q4 | curl (manual, no tool) | open.er-api.com /v6/latest/EUR + jsdelivr fawazahmed0 currency-api eur.json | EUR→VND changed from 28,985 to 28,400 (rounded; sources 28,411.71 / 28,302.55) → [[fx-eur-vnd-2026-11-14]]
- [2026-11-15] Q4 | WebSearch + WebFetch (subagent, no tool) | guide.michelin.com, wanderlog.com, joinpearl.co | 9 traditional Vietnamese picks (5 HN Michelin, 4 PQ Google 4.3+/800+), pins from Google Maps links → [[traditional-vietnamese-picks-2026-11-15]]
