<p align="center">
  <img src="./.github/assets/sk-quality-roofing-logo.png" alt="SK Quality Roofing logo" width="400">
</p>

# SK Quality Roofing — AI phone receptionist (demo)

Written for **owners and operators**—what this is, why it matters, and how to try it.

**Alex** is the voice assistant on your inbound line. Callers can **book**, **reschedule**, or **cancel** visits; for **new** work, you get a **yes/no on service area** from the property **ZIP** and only **job types you offer in that area**. They can ask **roofing questions** and walk through **the same topics and FAQs your website covers**—installs, repairs, materials, storm and insurance questions, timelines, licensing, and the rest—with **approved answers** that match your messaging. The goal is fewer calls lost to voicemail and less time spent repeating the same explanations at the front desk.

A **PDF** version of this page is in the repo: **[README.pdf](README.pdf)**. Regenerate after edits: `uv run python scripts/render_readme_pdf.py`.

## Try it

> **Phone:** **+1 (561) 250-5794**
>
> **Dialing / CRM:** `+15612505794`

Use any phone—regular voice call, no app. After the greeting, ask a question or say you’d like to **schedule**, **reschedule**, or **cancel**.

## Business value

- **Front desk:** **Book**, **reschedule**, **cancel**, and **FAQs** on the line—less **intake** and **phone tag**; staff stay free for **walk-ins**, **exceptions**, and **high-touch** calls.
- **High-value leads:** **Job type, issue, notes** can feed **CRM/workflows** so **replacements, big estimates, and heavy damage** get **desk or manager follow-up**.
- **After hours / busy lines:** **Route** calls here when **closed** or **no one’s free**; Alex captures **callback, address, issue, times**. **Routing** decides reachability—Alex **does not** read office hours. *Not connected to live calendar or dispatch in this build.*
- **ZIP menus:** Only **job types** allowed for that ZIP (`src/knowledge/regional_jobs.json`)—e.g. **Boca** includes **coatings / metal / flat**; **Delray** does not.
- **Reschedule / cancel:** By phone; **demo** completes with a **stub** visit; **production** ties to **CRM/calendar**.
- **FAQ:** **Approved** answers match **your site’s topics**—same messaging by voice.
- **Callback:** **SIP caller ID** (when available) to confirm the **best number**.

## Two-minute test drive

1. **Compare ZIPs**

   Say you want an estimate for a job. Use one call per address (or compare back-to-back):

   - **Delray — ZIP 33444**  
     `123 East Atlantic Ave, Delray Beach, FL 33444`
   - **Boca Raton — ZIP 33431**  
     `150 E Palmetto Park Rd, Boca Raton, FL 33431`

   Notice that **Boca Raton** includes **roof coatings** (and **metal** / **flat** options) in this demo, while **Delray Beach** does **not**—the menus are **ZIP-specific**.

2. **Out of area**

   - **ZIP 90210**  
     `9400 Wilshire Blvd, Beverly Hills, CA 90210`

   You should hear a **polite “outside our area”** message and **no booking**.
3. **FAQ only:** Ask *“What are common signs my roof needs repair?”* or *“How much does a roof replacement cost?”* You should get a **short, helpful** reply—not a sales script.
4. **Full booking:** Complete the flow with an in-area address, e.g. **123 East Atlantic Ave, Delray Beach, FL 33444**. You’ll get a **sample confirmation code** only; nothing is written to **ServiceTitan** or a **live calendar** in this build.
5. **Reschedule or cancel:** Give your **name** and confirm **callback number**—Alex **does not** ask for your old appointment time; the demo **always** shows **tomorrow** with a **9:00 AM–11:00 AM** window for **roof repair**, then **cancels** or offers **three new times** to **reschedule** (sample confirmations only).

## This build vs. Next steps

### This build (demo)

- **Booking** returns a **placeholder confirmation** (no real calendar or dispatch slot).
- **Reschedule** and **cancel** return **sample references**; the “existing visit” is a **fixed demo story** (tomorrow, 9:00 AM–11:00 AM, roof repair).
- **Customer lookup** is a **stub**—it always behaves like **no CRM match**, so every call can exercise the **new-caller** path.
- **ZIPs, regional job menus, and FAQ** are **real config** in the repo (easy to edit); **telephony and voice** run as in production-style hosting.

### Next steps (production)

- **Integrate CRM / FSM** (e.g. **ServiceTitan**) so **book**, **reschedule**, and **cancel** create or update **real jobs** and **appointments**.
- **Customer tracking** — replace **lookup_customer** with **live lookup** (phone, name, address) so **returning callers** and **existing jobs** are recognized when appropriate.
- **Real availability** — connect to your **schedule board** or **dispatch rules** so offered windows reflect **actual crew capacity**, not sample slots.
- **High-value routing** — use captured **job type, issue, and notes** to **tag or route** leads (e.g. full replacement, large estimate) for **front-desk or manager review** in the CRM.
- **Operational extras** as needed: **call recordings** or **transcripts** in your stack, **analytics**, **human handoff** queues, or **SMS/email** confirmations—same voice layer, richer backend.
- **Internal dashboards** — build **operator- or leadership-facing views** with **metrics that reflect Alex’s performance** (for example call volume, booking / reschedule / cancel completion, containment vs human handoff, handling time, after-hours mix, ZIP and job-type distribution, and quality signals from transcripts or sampling) so you can **iterate on prompts, routing, and staffing** with data.

**Config stays approachable:** **ZIP lists**, **regional job menus**, and **FAQ** remain **editable files**, so you can change **coverage and messaging** without rebuilding the **voice agent** from scratch.

## Bottom line

- **After hours & overflow** — **Fewer missed calls** when you **route** here off-hours or when **lines are busy**; Alex captures **who, where, issue, times**.
- **Front desk** — **Scheduling + FAQs** on Alex; team focuses on **exceptions** and **in-person** work.
- **ZIP truth** — Only **job types you allow per ZIP** (demo: **coatings** in **Boca**, not **Delray**).
- **One voice** — **FAQ-backed** replies aligned with **the website**.
- **Bigger jobs visible** — **Structured intake** can **flag** **replacements / major work** for **CRM** follow-up.
- **CRM-ready** — **SIP** improves **callback** confirmation; fields fit **ServiceTitan-style** systems.

**Config:** Tweak **ZIPs, menus, and FAQ** in **files**—no need to rebuild the **voice layer** every time the business shifts.

The assistant runs on **enterprise-grade real-time voice**, suitable for **cloud** deployment and **standard business phone** connections.

## Why this kind of work can move quickly

Projects like this one can be turned around fast because I work with **several AI software development agents** I **designed and built myself**—each **purpose-built for a different specialty** (for example voice and telephony, prompts and knowledge, tests and quality, or integrations). I **direct** them to the tasks that match their strengths, so parallel work and tight iteration are normal, not accidental. That setup is a big part of how I ship **AI-first** solutions on short timelines without sacrificing structure or reviewability.
