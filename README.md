<p align="center">
  <img src="./.github/assets/sk-quality-roofing-logo.png" alt="SK Quality Roofing logo" width="400">
</p>

# SK Quality Roofing — AI phone receptionist

Written for **owners and operators**—what this is, why it matters, and how to try it.

**Alex** is the voice assistant on your inbound line. Callers can **book**, **reschedule**, or **cancel** visits; for **new** work, you get a **yes/no on service area** from the property **ZIP** and only **job types you offer in that area**. They can ask **roofing questions** and walk through **the same topics and FAQs your website covers**—installs, repairs, materials, storm and insurance questions, timelines, licensing, and the rest—with **approved answers** that match your messaging. The goal is fewer calls lost to voicemail and less time spent repeating the same explanations at the front desk.

A matching **PDF** is in the repo: **[docs/executive-demo-brief.pdf](docs/executive-demo-brief.pdf)**.

## Try it

> **Phone:** **+1 (561) 250-5794**
>
> **Dialing / CRM:** `+15612505794`

Use any phone—regular voice call, no app. After the greeting, ask a question or say you’d like to **schedule**, **reschedule**, or **cancel**.

## Business value

- **After hours and busy lines:** The line can pick up **when you’re closed** or **when no one is free**, qualify the homeowner, and collect **callback number, address, issue, and time preferences** for your team. *This version is not connected to your live calendar or dispatch board.*
- **ZIP-based booking rules:** For **new** visits, Alex only offers **job types you’ve defined for that ZIP** (in the sample data, **33444** and **33435** show **different menus** on purpose).
- **Changes to existing visits:** Callers can **reschedule** or **cancel** by phone; the demo **always** completes those actions as if an appointment is on file (production would tie into your **CRM / calendar**).
- **Website FAQs on the phone:** Education and “I read this on your site” calls are handled with an **approved FAQ** that mirrors **the topics and question-and-answer content from your website**, so callers get **full coverage** of those subjects by voice—without staff repeating the same explanations.
- **Callback accuracy:** On standard **business phone (SIP)** service, the system can use **incoming caller ID** to double-check the best number to reach them.

## Two-minute test drive

1. **Compare ZIPs:** Say you want an inspection. Try **33444** (Delray in the sample), then **33435** (Boynton). Notice **which types of visits** Alex can book in each—the Boynton sample includes **more categories** (such as metal, flat, and coating work) than the Delray sample.
2. **Out of area:** Use **90210**. You should hear a **polite “outside our area”** message and **no booking**.
3. **FAQ only:** Ask *“What are common signs my roof needs repair?”* or *“How much does a roof replacement cost?”* You should get a **short, helpful** reply—not a sales script.
4. **Full booking:** Finish the flow with an in-area ZIP. You’ll get a **sample confirmation code** only; nothing is written to **ServiceTitan** or a **live calendar** in this build.
5. **Reschedule or cancel:** Give your **name** and confirm **callback number**—Alex **does not** ask for your old appointment time; the demo **always** shows **tomorrow, nine A M to eleven A M, roof repair**, then **cancels** or offers **three new times** to **reschedule** (sample confirmations only).

## This build vs. next step

**Right now,** **new** booking ends in a **placeholder confirmation**; **reschedule** and **cancel** return **sample references** too. **Customer lookup** always behaves like a **brand-new caller** so the demo always runs the full **new-booking** intake when relevant.

**When you’re ready to go live,** the **same questions and data fields** map cleanly to a **CRM or field platform** (for example **ServiceTitan**): replace the placeholders with **real integrations**. **ZIP lists, regional job menus, and FAQ** live in **simple files** you can update as coverage and offerings change—without rebuilding the voice system from scratch.

## Bottom line

- **After-hours coverage** — fewer calls lost to voicemail when you’re closed or everyone is on another line.
- **Consistent answers** — repeat education topics get the **same approved messaging** every time.
- **Tight control over geography and what you book** — you define **which ZIPs you serve** and **which visit types** are offered in each area.
- **Structured handoff** — details are captured in a form that maps cleanly to the **CRM and field tools** your team already uses.

Together, that means you can **adjust coverage and offers without rebuilding the voice system from scratch** as the business changes.

The assistant runs on **enterprise-grade real-time voice**, suitable for **cloud** deployment and **standard business phone** connections.

## Why this kind of work can move quickly

Projects like this one can be turned around fast because I work with **several AI software development agents** I **designed and built myself**—each **purpose-built for a different specialty** (for example voice and telephony, prompts and knowledge, tests and quality, or integrations). I **direct** them to the tasks that match their strengths, so parallel work and tight iteration are normal, not accidental. That setup is a big part of how I ship **AI-first** solutions on short timelines without sacrificing structure or reviewability.
