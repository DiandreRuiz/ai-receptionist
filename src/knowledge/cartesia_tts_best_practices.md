# Cartesia Sonic-3 — controllability and prompting

Use these practices for **text that will be synthesized** by **Sonic-3** (assistant lines read by TTS). They improve clarity and prosody; they complement SK receptionist content rules, not replace them.

## Punctuation

- Use appropriate punctuation throughout.
- Add punctuation where it helps phrasing, and **end each transcript-style utterance** with closing punctuation when possible.

## Dates

- Prefer dates in **MM/DD/YYYY** form (example: **04/20/2023**).

## Times

- Add a **space** between the time and **AM** or **PM**.
- Examples: **7:00 PM**, **7 PM**, **7:00 P.M.**

## Pauses

- To insert pauses, use **hyphens** (`-`) or **break tags** where a pause should occur.
- Break tags count as **one character**; you do **not** need spaces separating them from adjacent text—omitting extra spaces around break tags can **save credits**.

## Voice and language

- **Match the voice to the language.** Each voice works best with a given language; use the Cartesia playground to see which voices fit which language.

## Streaming

- **Stream inputs** for **contiguous** audio when generating speech in **separate chunks**; use **continuations** so separate generations still sound like one continuous utterance when that is the goal (align with how your pipeline chunks text).

## Custom pronunciations

- Specify **custom pronunciations** for **domain-specific** or **ambiguous** words: proper nouns, trademarks, and homographs spelled the same but pronounced differently (example: the city **Nice** vs. the adjective “nice”).

## Spelling out numbers and letters

- **Force spelling out** when clarity matters: **IDs**, **email addresses** read aloud, and other numeric or alphanumeric values where digit-by-digit or letter-by-letter delivery helps the caller.
