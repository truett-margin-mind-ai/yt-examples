# Interview Prep Guide

---

## Phase 1: The Role-Play Presentation (Executive Slide)

### How to Open (30 seconds)

Don't start with the data. Start with context and gratitude:

> "Thank you both for making time for this. We're six months into the partnership, and this is the moment to step back, look at the data together, and make sure this investment is delivering the value TechCorp expected. The short answer is: it is. Let me walk you through why."

This sets the tone -- you're a trusted advisor, not a vendor defending a product. It also frames the entire slide before they even read it.

### How to Walk Through the Slide (~3 minutes)

**Left column first (utilization):**

> "Let's start with adoption. 298 employees are actively coaching -- that's 60% of your licenses, six months in. And importantly, those users are averaging over 4 sessions each. This isn't a 'try it once and forget it' situation -- people are coming back. On current momentum alone, without deploying any new engagement strategies, we're projecting roughly 75% utilization by renewal. That's a strong trajectory."

**Right column (value):**

> "Now, is it working? The survey data says yes -- emphatically. Your NPS is +45, which puts this program in the top quartile. For reference, industry average for programs like this is around +30. Satisfaction is 4.3 out of 5, and the highest-rated dimension is 'my coach helps me achieve my goals' at 4.5. What I also want to call out is the survey response rate itself -- 52%. Typical is 25 to 35%. When more than half your active users take the time to respond, that tells you they care about this program."

**Bottom (recommendation):**

> "So -- should we renew? Our recommendation is yes. The foundation is strong. And with a targeted activation strategy starting now, we can strengthen that growth trend even further heading into renewal. There's real upside here."

---

### Likely Role-Play Questions (and How to Handle Them)

**1. "What about the discrepancy? Our count says 340, your dashboard says 298."**

This is almost certainly coming -- it's the first concern the HR Director flagged in the assignment. Stay calm, don't get defensive:

> "Great question, and I dug into this. Both numbers are actually correct -- they're measuring different things. Your 340 counts anyone who logged in or attended orientation. Our 298 counts users who've completed at least one coaching session. The gap of about 42 users represents people who've shown interest but haven't booked yet. That's actually good news -- it's a warm pipeline. These are people who've already opted in and just need a nudge to schedule their first session. One thing I'd recommend is that we align on a shared definition of 'active' going forward so we're always looking at the same number."

**2. "What about the coach response time complaints?"**

The second flagged concern. This is where your judgment shines:

> "I looked at this closely. There were 8 tickets about coach response time over the last 90 days -- but 5 of those came from a single user. So we're really talking about 4 unique people out of 298, which is about 1.3%. Total support volume is also very low -- 23 tickets across 90 days, only 2 escalations. The survey backs this up: coach responsiveness scored 3.8 out of 5 -- the lowest dimension, but still positive. My assessment is this is isolated, not systemic. That said, I'd want to pull actual platform response-time data to confirm, check whether those users share the same coach, and address the repeat filer directly -- possibly with a coach reassignment."

**3. "60% utilization -- why aren't we at higher adoption? We paid for 500."**

The CFO (Rebecca) may push on this. Don't apologize:

> "60% at six months is a strong mid-point. Programs like this don't hit full adoption on day one -- it's a ramp. What matters is the direction: we're growing at 12% month-over-month in new users, and the engagement depth is high with 4.2 sessions per user. The 77% who set up profiles tells us the intent is there. With a targeted activation strategy -- something we can partner on -- we can accelerate that conversion from profile setup to first session."

**4. "What would you recommend we do differently?"**

This is your moment to show strategic thinking:

> "Two things. First, let's partner on an activation campaign targeted at the ~90 users who've set up profiles but haven't booked a session. These are low-hanging fruit -- they've already opted in. That could be a nudge email from HR, a manager endorsement, or a simplified booking flow. Second, let's align on shared metrics and definitions now, so that by the next review we're looking at the same numbers and can focus the conversation on outcomes rather than reconciliation."

---

## Phase 2: The Memo Discussion (Break from Role-Play)

Devon said you'll "break from the role-play to discuss and answer questions regarding your approach and process." This means they'll shift from playing TechCorp execs to being BetterUp interviewers evaluating how you think.

### Likely Questions and How to Answer

**5. "Walk us through your process for the data discrepancy analysis."**

They want to hear your *method*, not just your answer. Show the steps:

> "My first instinct was to check whether this is a data problem or a definition problem -- and the definitions were right there in the data. TechCorp counts logins and orientation, we count completed sessions. But I wouldn't stop there. Before presenting that conclusion to a partner, I'd have my offshore analyst confirm the exact Looker definition, pull a login-only segment to verify the gap reconciles, check date-range alignment between the systems, and if possible, request the partner's user list for a 1:1 match. The goal is to walk in with confidence, not a hypothesis."

**6. "How did you decide the coach response time issue wasn't systemic?"**

This is the **judgment** evaluation criterion:

> "I separated signal from noise. Eight tickets sounds like a pattern until you notice 5 are from one person. That takes you from 8 reporters down to 4 unique users -- 1.3% of the active base. Then I cross-referenced with the survey: 3.8 out of 5 is the lowest score but still positive, and with 156 respondents, that's more representative than 4 ticket filers. Total ticket volume is also extremely low. All signals pointed the same direction. That said, I'd still want the platform response-time data to fully close the loop -- my conclusion is 'likely isolated, validate with one more data source.'"

**7. "Tell me about the scalability framework. How would you handle 20+ partners?"**

This is where the **pipeline framing** from the memo pays off:

> "The key insight is that every BVR follows the same workflow -- data assembly, QA, narrative, delivery. Right now that's all manual and analyst-driven. My approach is to automate the first two stages -- pull the data automatically, run reconciliation checks and threshold-based flags -- so that the offshore team is only doing QA on pre-assembled packages, and my time goes entirely to narrative and judgment. I've done this before: at a previous company, I automated a multi-stakeholder weekly business review that was consuming 40 hours a week across four people. Consolidated the sources into a warehouse, built transformation models, and auto-generated reports. Took it down to under an hour. Same playbook applies here."

**8. "How would you use AI in this role?"**

Given how AI-forward the role is, expect this:

> "AI is most valuable in the assembly and first-draft layers. Auto-populating BVR templates, summarizing support ticket themes, generating a first-pass narrative from structured data -- those are all things AI handles well with human review. Where I'd be more cautious is in the judgment layer: interpreting anomalies, deciding what to escalate, and building the executive story. That still needs a human. I'd also use AI to train the offshore team -- building validation workflows so they can quality-check AI outputs rather than creating everything from scratch."

**9. "What would success look like for you in the first 90 days?"**

You noted this question from your interview with Ashley. Tie it back to what they're building:

> "In the first 30 days, I'd want to understand the current state -- how BVRs are done today, what data sources exist, and where the pain points are for CSMs. I'd map the full data ecosystem: Looker, Salesforce, Vitally, survey tools, support systems. In days 30-60, I'd build the first version of a standardized BVR template and the triage framework for the offshore team -- what they can handle vs. what needs me. By day 90, I'd want at least one BVR running through the new pipeline end-to-end, with a clear picture of what to automate next."

---

## Mapping to Their Evaluation Criteria

Keep these in mind as you answer anything:


| Criterion                     | Where You Demonstrate It                                                    |
| ----------------------------- | --------------------------------------------------------------------------- |
| **Systems thinking**          | The funnel (500 → 387 → 340 → 298), understanding why systems conflict      |
| **Executive communication**   | The slide itself -- clean, narrative-driven, benchmarked                    |
| **Process design**            | The BVR pipeline framework, the phased automation approach                  |
| **Judgment**                  | Coach response time: signal vs. noise, knowing what NOT to put on the slide |
| **Quality orientation**       | Catching the definitional root cause, the 5-from-same-user detail           |
| **Practical problem-solving** | Working with imperfect data, the Hitch WBR as proof you've done it          |


---

## General Tips

- **Don't read the slide.** You know the data cold. Talk to Ashley and Rebecca like colleagues, not an audience.
- **Pause after the recommendation.** Let them react. Don't fill silence.
- **When challenged, don't backpedal.** "Great question" + direct answer + supporting evidence. Every concern flagged in the assignment is something they'll bring up. You have the answers.
- **In Phase 2, show your thinking, not just your conclusions.** They want to see *how* you got there, not just that you got there.
- **Reference the Hitch story naturally** -- don't force it, but when they ask about scalability or automation, that's your moment. Keep it to 30-60 seconds: problem, what you did, result.

