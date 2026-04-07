# SK Quality Roofing — AI phone receptionist (demo)

Written for **owners and operators**—what this is, why it matters, and how to try it.

**Alex** is the voice assistant on your inbound line. Callers can **book**, **reschedule**, or **cancel** visits; for **new** work, you get a **yes/no on service area** from the property **ZIP** and only **job types you offer in that area**. They can ask **roofing questions** and walk through **the same topics and FAQs your website covers**—installs, repairs, materials, storm and insurance questions, timelines, licensing, and the rest—with **approved answers** that match your messaging. The goal is fewer calls lost to voicemail and less time spent repeating the same explanations at the front desk.

A matching **PDF** is in this folder: **[executive-demo-brief.pdf](executive-demo-brief.pdf)**.

## Try it

> **Phone:** **+1 (561) 250-5794**
>
> **Dialing / CRM:** `+15612505794`

Use any phone—regular voice call, no app. After the greeting, ask a question or say you’d like to **schedule**, **reschedule**, or **cancel**.

## Business value

- **Less load on the front desk:** Alex **books**, **reschedules**, and **cancels** appointments and answers **repeat “website” questions**, so your team spends less time on **phone tag** and **intake** and more on **walk-ins, exceptions, and high-touch work**. Routine scheduling and FAQ handling move to the line without replacing judgment where you still want a human.
- **Flag high-value jobs for review:** The same **structured data** you capture (job type, issue description, notes) can feed **workflows or your CRM** so calls that look like **full replacements, big-ticket estimates, or complex damage** are **marked for front-desk or manager follow-up**—so the **largest revenue opportunities** get a deliberate second look, not lost in the noise.
- **After hours and busy lines:** When you **route** inbound calls here **after you’re closed** or **when no one is free**, Alex can pick up, qualify the homeowner, and collect **callback number, address, issue, and time preferences** for your team. The agent **does not read your office hours**—who reaches Alex depends on your **phone routing**. *This version is not connected to your live calendar or dispatch board.*
- **ZIP-based booking rules:** For **new** visits, Alex only offers **job types** from **`get_bookable_jobs`** for that ZIP (from `src/knowledge/regional_jobs.json`). Menus differ by area—for example **Boca Raton** includes **roof coatings**, **metal**, and **flat** work; **Delray Beach** stays to **installation**, **inspection**, **repair**, and **shingle/tile** options only (with shorter labels like **Installation** / **Inspection** in that region).
- **Changes to existing visits:** Callers can **reschedule** or **cancel** by phone; the demo **always** completes those actions as if an appointment is on file (production would tie into your **CRM / calendar**).
- **Website FAQs on the phone:** Education and “I read this on your site” calls are handled with an **approved FAQ** that mirrors **the topics and question-and-answer content from your website**, so callers get **full coverage** of those subjects by voice—without staff repeating the same explanations.
- **Callback accuracy:** On standard **business phone (SIP)** service, the system can use **incoming caller ID** to double-check the best number to reach them.

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

**Config stays approachable:** **ZIP lists**, **regional job menus**, and **FAQ** remain **editable files**, so you can change **coverage and messaging** without rebuilding the **voice agent** from scratch.

## Bottom line

- **After hours and overflow** — when you **send calls** to this line **after hours** or **when staff are tied up**, Alex can answer, capture **who, where, what’s wrong, and preferred times**, and cut **voicemail abandonment** (routing is yours; the agent does not infer open/closed hours).
- **Less load on the front desk** — **book**, **reschedule**, and **cancel** on the phone plus **repeat FAQ** handling, so your team spends less time on **phone tag** and **intake** and more on **exceptions and high-touch** work.
- **ZIP-accurate offers** — only **job types you allow per ZIP** (demo: e.g. **roof coatings** in **Boca Raton**, not in **Delray**), so promises match **how you operate by market**.
- **Website-aligned answers** — callers get **approved FAQ coverage** by voice for the **same topics** they’d read on your site—**consistent messaging** without staff repeating long explanations.
- **High-value jobs surfaced** — **structured fields** (job type, issue, notes) can feed **CRM or workflows** so **big replacements, heavy damage, or large estimates** are **flagged for front-desk or manager follow-up**.
- **Accurate callbacks and CRM-ready data** — **SIP caller ID** helps confirm the **best number**; captured details **map cleanly** to **ServiceTitan-style** systems.

Together, that means you can **adjust ZIPs, menus, and FAQ in simple files** and **iterate** without rebuilding the **voice layer** from scratch as the business changes.

The assistant runs on **enterprise-grade real-time voice**, suitable for **cloud** deployment and **standard business phone** connections.
