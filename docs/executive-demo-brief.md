# SK Quality Roofing — AI receptionist (demo)

This document describes a **proof-of-concept inbound phone agent** built as an interview take-home. It shows how a residential roofing company could use AI to **answer calls, handle common questions, and guide people toward booked appointments**—without requiring a larger front desk around the clock.

---

## Try the demo

**Call:** **+1 (561) 250-5794**

You will have a **normal voice conversation** with the AI receptionist (Alex) from any phone. No app required.

*Technical format (for systems):* `+15612505794`

---

## What the agent can do

**Natural phone conversation.** The agent listens and speaks in real time, so callers can explain leaks, storm worries, or scheduling needs the way they would to a person.

**After hours and overflow.** Software does not clock out. On a live phone line, this kind of agent can **answer when the office is closed**, on weekends, or when lines are busy—**qualifying the caller**, capturing details, and walking through **appointment-style booking steps** so your team starts Monday with structured leads instead of missed calls. *(This demo is not connected to your real calendar; it is built to show the experience and workflow.)*

**Service area and “what we can book” by location.** When someone wants a visit, the agent uses the property’s **ZIP code** to check whether you serve that area and **which types of jobs are bookable there** (for example, certain regions in the demo include a wider menu—metal, flat, coatings—while others intentionally list a narrower set). That keeps promises aligned with how you actually operate in each market.

**FAQ-style calls without tying up staff.** Many calls are general education: costs at a high level, storm damage, how installs work, licensing questions, and so on. The agent draws on a **curated FAQ** aligned with your messaging so those callers get consistent, approved answers and only escalate when it makes sense.

**Caller ID when the network provides it.** On typical business SIP phone setups, the agent can **see the inbound number** to confirm callbacks—reducing typos and speeding up booking.

---

## Try this (2-minute tour)

Use these prompts when you call **+1 (561) 250-5794**:

1. **Different services by ZIP.** Say you want to schedule an inspection and give ZIP **33444** (Delray Beach in the demo data). Listen to which visit types the agent can offer. Call again (or continue) and try ZIP **33435** (Boynton Beach)—the demo allows **additional** bookable categories there (for example metal, flat, and coating work) that Delray does not list in this dataset.
2. **Outside the service area.** Say you need someone at a property in ZIP **90210**. The agent should politely explain the property is **outside the served areas** in this demo and not book a visit.
3. **FAQ instead of booking.** Ask something like **“What are common signs my roof needs repair?”** or **“How much does a roof replacement cost?”** You should get a short, helpful answer grounded in the approved FAQ—not a sales monologue.
4. **Full booking path.** Walk through scheduling with an in-area ZIP. The demo **confirms** a visit with a **sample confirmation** (it does not write to a real schedule).

---

## Demo today vs. production tomorrow

**What is simulated in this build**

- **Appointment booking** returns a **demo confirmation** (placeholder reference), not a live slot in ServiceTitan or another system.
- **Customer lookup** behaves like an empty CRM in the demo so the flow always exercises “new caller” handling.

**What is already “production-shaped”**

- The **steps and data fields** (name, address, phone, job type, issue summary, date and time window, optional claim number, etc.) mirror how you would hook into a **CRM / FSM such as ServiceTitan**: replace the stubs with real API calls, and the same conversation becomes operational.

**Why that matters for you**

- **Business knowledge** (service ZIPs, regional job menus, FAQ) lives in **editable files**, so you can change service areas and offerings **quickly** as the company grows.
- The voice layer stays stable while you **iterate**: new policies, new markets, seasonal scripts, or deeper CRM automation.

---

## Closing thought

The built world runs on **phones, schedules, and trust**. This demo is a concrete example of bringing **AI-first** tooling to that reality: **capture demand after hours**, **deflect repetitive questions**, **route by geography and service line**, and **hand off clean data** to the systems your teams already use—so you deliver value fast and keep improving without rebuilding from scratch.

*Infrastructure note:* Built on **LiveKit** enterprise-grade real-time voice, suitable for cloud deployment and telephony integration.
