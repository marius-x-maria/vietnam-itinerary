---
name: vietnam-itinerary-tools
description: Map of Content — deterministic scripts for the vietnam-itinerary project
tags: [index, moc, vietnam-itinerary]
---

# Tools — Vietnam Itinerary

| Tool | What it answers |
|---|---|
| `encrypt_private.py` | Encrypts `private/family-o.local.html` into the `PRIVATE_O` block of `index.html` with `FAMILY_O_CODE` from `.env`, then verifies no private text is left in clear text. `--json`, exit 0/1/2. Needs `cryptography`. |
