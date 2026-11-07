# Public screenshot approval manifest

This file is intentionally empty until an authorised reviewer has approved a **sanitised** image for publication.

For each approved image, add exactly one line:

`assets/screenshots/example.png <64-character lowercase SHA-256 of the final image bytes>`

The automated publication gate verifies that the approved bytes have not changed. Any edit, recompression or replacement requires a fresh human review and a new digest. A digest **does not** prove the reviewer had authority to release the image; record the reviewer, date, provenance, sanitisation actions and publication decision in the **private** portfolio-control evidence register, never in this public manifest.

Do not commit raw captures, client identifiers, employee details, private URLs or unreviewed screenshots. The static website's illustrated walkthroughs remain **MOCK-ONLY** until independently verified.
