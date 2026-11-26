---
type: pitchcraft-session
saved_at: 2026-03-04T16:40:00Z
stage: final
---

# Session: Cutting CI build times in monorepos

## Context
- **Event:** Industry/tech conference, BuildCon
- **Theme:** Developer productivity at scale
- **Session type:** Talk (30 minutes)
- **Audience level:** Practitioners
- **Tone:** Practical and plain-spoken
- **Language:** English
- **Starting point:** From scratch
- **Limits:** title up to 80 chars, abstract up to 150 words
- **Guardrails:** No buzzwords, no emojis
- **Writing style:** none
- **Idea:** Three changes that took a large monorepo's pipeline from 45 to 12 minutes.
- **Key takeaway:** Measure before caching; most of the time is not where you expect.
- **Must mention:** the open-source profiling script linked in the final slide
- **Style notes:** short sentences, concrete numbers

## Title
- **Status:** locked
- **Current:** From 45 to 12 Minutes: Fixing a Slow Monorepo Pipeline (54 chars)
- **Rejected:** "Is Your CI Lying to You?", "The Art of the Fast Build"

## Abstract
- **Version:** 3
- **Format:** Plain text

Your pipeline takes 45 minutes and nobody remembers why. We'll walk through how one large monorepo got to 12 without changing tools: profile first, then fix test selection, then fix caching. Along the way you'll see which "obvious" optimizations made things slower.

You'll leave with a checklist for profiling your own pipeline, three metrics worth tracking, and a script you can run on Monday. Aimed at engineers who own or depend on a CI system, no prior monorepo experience needed.

## Final
- **Title:** From 45 to 12 Minutes: Fixing a Slow Monorepo Pipeline (54 chars)
- **Abstract:** (80 words)

Your pipeline takes 45 minutes and nobody remembers why. We'll walk through how one large monorepo got to 12 without changing tools: profile first, then fix test selection, then fix caching. Along the way you'll see which "obvious" optimizations made things slower.

You'll leave with a checklist for profiling your own pipeline, three metrics worth tracking, and a script you can run on Monday. Aimed at engineers who own or depend on a CI system, no prior monorepo experience needed.
