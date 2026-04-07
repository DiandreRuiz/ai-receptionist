# SK Quality Roofing — AI phone receptionist: project overview

Written for **owners and operators**—what this is, why it matters, and how to try it, in plain English.

**Alex** is the voice assistant on your inbound line. Callers can ask **roofing questions**, get a **yes/no on service area** from the property **ZIP**, hear only **job types you offer in that area**, and go through **scheduling steps** (contact details, address, what’s wrong, preferred times). The goal is fewer calls lost to voicemail and less time spent answering the same general questions at the front desk.

A matching **PDF** is in this folder: **[executive-demo-brief.pdf](executive-demo-brief.pdf)**.

## Try it

> **Phone:** **+1 (561) 250-5794**
>
> **Dialing / CRM:** `+15612505794`

Use any phone—regular voice call, no app. After the greeting, ask a question or say you’d like to schedule.

## Business value

- **After hours and busy lines:** The line can pick up **when you’re closed** or **when no one is free**, qualify the homeowner, and collect **callback number, address, issue, and time preferences** for your team. *This version is not connected to your live calendar or dispatch board.*
- **ZIP-based booking rules:** Alex only offers **visit types you’ve defined for that ZIP** (in the sample data, **33444** and **33435** show **different menus** on purpose).
- **FAQ-heavy calls:** Typical education topics—**ballpark cost context**, **storm damage**, **how installs work**, **licensing**—pull from a **curated FAQ** so answers stay aligned with your messaging.
- **Callback accuracy:** On standard **business phone (SIP)** service, the system can use **incoming caller ID** to double-check the best number to reach them.

## Two-minute test drive

1. **Compare ZIPs:** Say you want an inspection. Try **33444** (Delray in the sample), then **33435** (Boynton). Notice **which types of visits** Alex can book in each—the Boynton sample includes **more categories** (such as metal, flat, and coating work) than the Delray sample.
2. **Out of area:** Use **90210**. You should hear a **polite “outside our area”** message and **no booking**.
3. **FAQ only:** Ask *“What are common signs my roof needs repair?”* or *“How much does a roof replacement cost?”* You should get a **short, helpful** reply—not a sales script.
4. **Full booking:** Finish the flow with an in-area ZIP. You’ll get a **sample confirmation code** only; nothing is written to **ServiceTitan** or a **live calendar** in this build.

## This build vs. next step

**Right now,** booking ends in a **placeholder confirmation**, and **customer lookup** always behaves like a **brand-new caller** so the demo always runs the full intake.

**When you’re ready to go live,** the **same questions and data fields** map cleanly to a **CRM or field platform** (for example **ServiceTitan**): replace the placeholders with **real integrations**. **ZIP lists, regional job menus, and FAQ** live in **simple files** you can update as coverage and offerings change—without rebuilding the voice system from scratch.

## Bottom line

You get **after-hours coverage**, **consistent answers** on repeat topics, **tight control over geography and what you book**, and **structured handoff** to the tools your team already runs on—without starting over every time you refine the business. The runtime uses **enterprise-grade real-time voice**, suitable for **cloud** hosting and **standard business phone** connections.
