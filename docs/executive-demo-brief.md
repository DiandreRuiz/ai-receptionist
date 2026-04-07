# SK Quality Roofing — AI phone receptionist: project overview

Plain-language summary for **owners and operators**. **Alex** is an inbound **voice** assistant on the phone: it answers **roofing questions**, checks **service area by ZIP**, matches **bookable job types to location**, and **guides callers through scheduling steps**—cutting voicemail loss and repeat FAQ load on staff.

**PDF:** **`executive-demo-brief.pdf`** (same folder).

---

## Try it

**Call +1 (561) 250-5794** (`+15612505794`). Normal voice call; no app.

---

## Business value

- **24/7-style coverage:** Can answer **after hours** and when lines are busy, qualify the caller, and capture **contact, address, issue, and time preferences** for the team. *(Not wired to your live calendar in this build.)*
- **ZIP-aware offers:** Only suggests **job types you define per area** (sample data differs by market—e.g. broader menus vs. narrower).
- **FAQ offload:** **Curated answers** for common education calls (cost context, storm, process, licensing) so staff focus on real opportunities.
- **Caller ID:** On typical **business phone (SIP)** setups, can confirm **callback number** from the inbound line.

---

## Two-minute test drive

1. **33444** (Delray sample) vs **33435** (Boynton sample)—compare which visit types are bookable.
2. **90210**—polite **out-of-area**; no booking.
3. Ask **“Signs my roof needs repair?”** or **replacement cost**—short **FAQ-style** answer.
4. Full book flow—in-area ZIP ends in a **sample confirmation** only (no ServiceTitan / live calendar yet).

---

## This build vs. next step

**Today:** Booking returns a **placeholder confirmation**; customer lookup is a **stub** (new-caller path every time).

**Next:** Same **fields and flow** are **CRM/FSM-ready** (e.g. **ServiceTitan**)—swap stubs for **APIs**. **ZIPs, job menus, and FAQ** stay in **editable files** for fast updates.

---

## Bottom line

**Capture after-hours demand**, **standardize answers**, **route by geography and service**, and **hand off structured data** to tools you already use—without rebuilding from scratch. Built on **enterprise real-time voice** for **cloud** and **standard telephony**.
