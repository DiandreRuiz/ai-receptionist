# SK Quality Roofing — AI phone receptionist: project overview

This note is a **plain-language summary** of an **inbound AI phone receptionist** for SK Quality Roofing. It is meant for owners and operators who want the business picture without technical detail.

The system answers **real phone calls** with a natural voice assistant (**Alex**). It helps homeowners with **common roofing questions**, checks **whether you serve their area**, aligns **what can be scheduled** with **local rules**, and **walks callers through booking-style steps** so fewer calls die on voicemail and less front-desk time goes to repeat questions.

A **PDF** version of this overview is available in the same folder: **`executive-demo-brief.pdf`**.

---

## Experience it yourself

**Call:** **+1 (561) 250-5794**

You will have a normal **voice conversation** with Alex from any phone. No app is required.

For phone systems and CRM fields, the number in international format is **`+15612505794`**.

---

## What it does for the business

**Sounds like a person, works at machine scale.** Callers describe leaks, storm damage, or scheduling needs in their own words; the assistant responds in real time by voice.

**After hours and busy periods.** The line can **answer when the office is closed**, on weekends, or when staff are tied up—**qualifying** the caller, capturing **name, address, issue, and preferred times**, and moving them toward a **confirmed visit window** so your team starts the day with **organized leads** instead of **lost calls**. *(In the current build, calendar connection is illustrated but not tied to your live dispatch board.)*

**Right service, right ZIP.** When someone wants a visit, the assistant uses the property’s **ZIP code** to confirm **coverage** and to know **which types of jobs you offer in that area** (for example, some areas in the sample data include a **broader** list—metal, flat, coatings—while others show a **tighter** menu). That keeps **promises** aligned with **how you actually operate** by market.

**Frees your people from “website” calls.** Many inbound calls are **education**, not jobs: rough cost context, storm worries, how installs work, licensing, timelines. The assistant uses a **curated FAQ** aligned with your messaging so answers stay **consistent and approved**, and only **human follow-up** when it adds value.

**Callback number accuracy.** On standard business phone (SIP) connections, the system can use the **inbound caller ID** to confirm the best number to call back—fewer wrong numbers and faster booking.

---

## Suggested two-minute test drive

When you call **+1 (561) 250-5794**, try:

1. **Different services by area.** Ask to schedule an inspection and give ZIP **33444** (Delray Beach in the sample data). Notice which visit types are offered. Call again or continue with ZIP **33435** (Boynton Beach)—the sample allows **additional** bookable categories there (such as metal, flat, and coating work) that the Delray sample list does not include.
2. **Outside the service area.** Ask for service at ZIP **90210**. You should hear a polite explanation that the property is **outside the served areas** in this sample and that a visit will not be booked.
3. **Questions instead of booking.** Ask something like **“What are common signs my roof needs repair?”** or **“How much does a roof replacement cost?”** You should get a **short, helpful** answer grounded in the **approved FAQ**, not a hard sell.
4. **Full scheduling path.** Complete the flow with an in-area ZIP. The build **confirms** with a **sample confirmation reference**; it does **not** write to a live calendar or ServiceTitan yet.

---

## What’s in this build vs. what’s next

**Simulated for now**

- **Booking** returns a **sample confirmation** (placeholder reference), not a real slot in ServiceTitan or another system.
- **Existing customer lookup** behaves like an **empty CRM** so every run exercises **new-caller** handling.

**Already shaped for production**

- The **data captured** (name, address, phone, job type, issue summary, date and time window, optional claim number, and notes) matches how you would **connect to a CRM / field platform such as ServiceTitan**: replace the placeholders with **real APIs**, and the **same conversation** becomes operational.

**Why that matters**

- **Coverage, job menus, and FAQ** live in **editable files**. When you add ZIPs, change offerings, or update messaging, you can do it **quickly** without rebuilding the whole system from scratch.
- The **voice layer** can stay stable while you **iterate** on policy, regions, scripts, and **deeper automation** with your existing tools.

---

## Closing

Homes and roofs still run on **phones, schedules, and trust**. This project shows how **AI-first** phone support can **capture demand after hours**, **answer repeat questions consistently**, **route by geography and service line**, and **hand off clean information** to the systems your team already uses—so you see **value quickly** and can **improve continuously** without starting over.

The implementation uses **enterprise-grade real-time voice** infrastructure suitable for **cloud deployment** and **standard business phone** integration.
