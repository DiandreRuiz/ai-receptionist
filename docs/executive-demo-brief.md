# SK Quality Roofing — AI phone receptionist

## Project overview

This one-pager is for **owners and operators**: what the system does, why it matters, and how to try it—without technical jargon.

**Alex** answers **inbound phone calls** in natural speech. It handles **common roofing questions**, checks **whether the property is in your service area** (by **ZIP code**), offers only **job types you allow for that area**, and **walks callers through scheduling** (name, address, issue, preferred times). That reduces **voicemail abandonment** and keeps **repeat “website questions”** off your front desk.

A **PDF** copy of this note is saved alongside it as **`executive-demo-brief.pdf`**.

## Try it

> **Phone:** **+1 (561) 250-5794**
>
> **Systems / CRM:** `+15612505794`

Call from any phone—normal voice conversation; no app. You should hear a short greeting, then you can ask questions or say you want to schedule.

## What callers get

- **Human-style conversation:** Callers explain leaks, storms, or scheduling in their own words; Alex responds in real time by voice.
- **After hours and overflow:** The same line can **answer when the office is closed** or when everyone is on another call, **capture lead details**, and **offer appointment-style windows** so the crew starts with **structured follow-ups** instead of missed calls. *(This build does not connect to your live dispatch calendar.)*
- **ZIP-based routing:** Service area and **which visit types are bookable** come from **rules you maintain** (in the sample, **33444** vs **33435** illustrates **different menus** by area).
- **FAQ handling:** Education calls—rough cost context, storm damage, how installs work, licensing—draw on a **curated FAQ** so messaging stays **consistent** with what you approve.
- **Caller ID (typical business phone):** On **SIP** lines, the inbound number can be used to **confirm the best callback number**.

## Try this (about two minutes)

1. **Different menus by ZIP:** Say you want an inspection. Try **33444** (Delray Beach in the sample), then **33435** (Boynton Beach). Listen for **which job types** Alex can book in each—Boynton’s sample list includes **more categories** (e.g. metal, flat, coating) than Delray’s.
2. **Out of area:** Give **90210**. Expect a **polite decline**; no booking.
3. **FAQ only:** Ask **“What are common signs my roof needs repair?”** or **“How much does a roof replacement cost?”**—short, informative answers, not a hard pitch.
4. **Full booking:** Complete the flow with an in-area ZIP. You get a **sample confirmation reference** only—**not** a real ServiceTitan or calendar entry **yet**.

## This build vs. next step

**In this build:** **Booking** returns a **placeholder confirmation**; **customer lookup** is a **stub** so every call exercises the **new-caller** path.

**Ready for production:** The **information collected** matches what you’d send to a **CRM or field platform** (e.g. **ServiceTitan**): swap stubs for **real APIs**, and the same voice flow goes live. **ZIP lists, regional job menus, and FAQ** stay in **editable files** so you can **adjust coverage and messaging quickly** without rewriting the whole system.

## Summary

**Capture demand after hours**, **answer repeat questions consistently**, **enforce geography and service rules**, and **hand off clean data** to the tools your team already uses. Built on **enterprise-grade real-time voice** for **cloud** deployment and **standard business telephony**.
