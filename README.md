<p align="center">
  <img src="./.github/assets/sk-quality-roofing-logo.png" alt="SK Quality Roofing logo" width="400">
</p>

# SK Quality Roofing — AI phone receptionist (demo)

Written for **owners and operators**—what this is, why it matters, and how to try it.

**Alex** is the voice assistant on your inbound line. Callers can **book**, **reschedule**, or **cancel** visits; for **new** work, you get a **yes/no on service area** from the property **ZIP** and only **job types you offer in that area**. They can ask **roofing questions** and walk through **the same topics and FAQs your website covers**—installs, repairs, materials, storm and insurance questions, timelines, licensing, and the rest—with **approved answers** that match your messaging. The goal is fewer calls lost to voicemail and less time spent repeating the same explanations at the front desk.

## Executive summary

**Alex** answers your inbound line like a trained front-desk teammate: callers can **schedule**, **reschedule**, or **cancel**; for new work, **address and ZIP** determine **whether you serve the area** and which **job types** apply. Callers can also ask **roofing questions** using **the same approved topics and FAQs as your website**—so answers stay **on-message** and staff spend less time repeating basics.

| | |
| --- | --- |
| **Why it matters** | Fewer calls lost to voicemail or hold; **structured intake** (who, where, what’s wrong, when to call back) for **CRM follow-up**; **after-hours and overflow** without adding headcount. |
| **What this demo is** | **Real voice and telephony** with **sample** bookings and visits—so you can stress-test the experience without touching production calendars or dispatch. |
| **What production adds** | Hook up **your CRM / field service** (e.g. **ServiceTitan**), **real availability**, and **live customer match**—same voice layer, real data. |

---

## Try it now

> **Phone:** **+1 (561) 250-5794**  
> **E.164 / CRM:** `+15612505794`

Use any phone—voice call, no app. After the greeting, ask a **roofing question** or say you want to **schedule**, **reschedule**, or **cancel**.

---

## What to listen for (about two minutes)

These calls show **ZIP-specific menus** and **out-of-area handling**—the important part is that **service rules follow your configuration**, not a generic script.

1. **Same ask, two ZIPs (menus differ)**  
   Say you want an **estimate**. Try one call per address (or back-to-back):

   - **Delray Beach — ZIP 33444** — `123 East Atlantic Ave, Delray Beach, FL 33444`  
   - **Boca Raton — ZIP 33431** — `150 E Palmetto Park Rd, Boca Raton, FL 33431`  

   In this demo, **Boca** includes options such as **roof coatings** (and **metal** / **flat**) that **Delray** does not—**job types are tied to service area**.

2. **Out of area** — **ZIP 90210** with e.g. `9400 Wilshire Blvd, Beverly Hills, CA 90210`  
   You should hear a **clear “outside our area”** response and **no booking**.

3. **FAQ** — e.g. *“What are common signs my roof needs repair?”* or *“How much does a roof replacement cost?”*  
   Short, factual tone—not a hard sell.

4. **Booking (sample only)** — Complete intake with an in-area address (e.g. Delray example above). You get a **sample confirmation code**; **nothing is written to ServiceTitan or a live calendar** in this build.

5. **Reschedule / cancel (sample only)** — The demo assumes a **fixed “existing visit”** (tomorrow morning, roof repair) so every caller can run the flow. You’ll get **sample** confirmations, not real schedule changes.

---

## Demo vs production (decision-ready)

### Included in this demo

- **Voice** and **phone path** representative of a production-style deployment.  
- **Regional rules** (ZIPs, job-type menus, FAQ) driven by **real configuration** in the repo—adjustable without rewriting the core agent.  
- **Booking / reschedule / cancel** return **placeholders** so you can evaluate conversation quality safely.

### Typical path to production

- **CRM / FSM integration** so appointments and jobs are **created and updated for real**.  
- **Schedule and dispatch** so offered times reflect **crew capacity**, not samples.  
- **Customer recognition** (phone / account) for **returning callers** and **existing work**.  
- **Routing and alerts** so **large jobs or replacements** surface to **desk or manager** workflows.  
- **Optional:** recordings, transcripts, analytics, SMS/email confirmations, handoff queues—same assistant, **your** operational stack.

---

## Platform note

The assistant uses **real-time voice** suitable for **cloud** hosting and **standard business telephony**. Callback quality benefits from **SIP caller ID** when your carrier provides it.

---

## Ongoing changes (no rebuild every time)

**Service areas**, **job-type menus**, and **FAQ content** are maintained as **editable configuration**—you can adjust **coverage and messaging** as the business changes, without throwing away the voice layer.

---

*Maintainers: after editing this README, refresh the PDF with `uv run python scripts/render_readme_pdf.py`.*
