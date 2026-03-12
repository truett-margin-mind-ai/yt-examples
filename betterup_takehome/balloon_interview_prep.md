# Balloon Interview Prep Guide

**Format:** Behavioral interviews, STAR format, conversational and open-ended.
**These are role-agnostic** — every BetterUp candidate does these. They're not about the take-home.

---

## Interview 1: Extreme Owner & Craftsperson (10:30–11:30 AM CST)

**Interviewer:** Jason Moon — Staff Frontend Engineer, 5+ years at BetterUp, 25+ years in software (jQuery contributor, VMware, Digital River). As a senior engineer with deep tenure, he values precision, quality, and ownership culture. He's seen what craftsmanship looks like over decades.

**What they're evaluating:**

- **Extreme Ownership:** Do you take full responsibility for outcomes — including failures? Do you own problems beyond your job description? Do you lead without being asked?
- **Craftsperson:** Do you care deeply about quality? Do you sweat the details? Do you continuously improve your craft? Do you hold yourself to a high bar even when no one is watching?

---

## Interview 2: Builder (12:00–12:45 PM CST)

**Interviewer:** Hunter Black — Principal Behavioral Scientist, 10+ years at BetterUp (employee ~early days), organizational psychologist, coaching science expert. He literally studies these competencies for a living. He'll be attuned to self-awareness, intellectual honesty, and growth signals.

**What they're evaluating:**

- **Builder:** Do you create things from scratch? Do you thrive in ambiguity? Do you take an idea from 0→1? Are you resourceful when there's no playbook?

---

## STAR Format Reminder

Every answer should follow this structure. Aim for 2–3 minutes per answer.


| Element       | What to say                                                   | Time      |
| ------------- | ------------------------------------------------------------- | --------- |
| **Situation** | Set the scene — company, role, stakes, constraint             | 15–20 sec |
| **Task**      | What was your specific responsibility or challenge            | 10–15 sec |
| **Action**    | What YOU did (not the team) — be specific                     | 60–90 sec |
| **Result**    | Measurable outcome + what you learned or would do differently | 20–30 sec |


**Kush's closing formula (use everywhere):**

> "The goal was to [measurable outcome], protect [stakeholder trust], and ensure [scalable capability] without [bottleneck risk]."

**Always do at the start:** Restate or paraphrase the question, acknowledge the constraint or stakes.
**Always do at the end:** Name a measurable outcome, connect to strategic alignment, invite follow-up.

---

## Kush's Focus Areas — Mapped to Your Stories

These are the question types Kush expects. Each one maps to a story you already have.

---

### 1. Ownership Mentality

*"Tell me about a time you were wrong about an analysis."*
*Tests: ego + accountability*

**Use: Regression Multicollinearity Mistake at Hitch**

> **S:** At Hitch, we were trying to understand what operational inputs actually drove margins on a day-to-day basis. This was a high-stakes question — the answer would shape where the company focused its energy.
>
> **T:** I ran a regression analysis across several variables to identify which inputs had the strongest correlation with daily margins. I found three primary drivers: round-trip fill rate, empty returns, and driver pay.
>
> **A:** When I looked at the coefficients, driver pay appeared to have as much significance as fill rate and empty returns *combined*. So I presented that finding to my manager — essentially saying driver pay was the dominant lever we should focus on. He was immediately skeptical, and he was right to be. The problem was multicollinearity: round-trip fill rate and empty returns are inherently correlated — when fill rate goes up, empty returns go down. Because they move together, the regression splits their explanatory power between them, muting each one's individual significance. So it looked like driver pay was the dominant factor when really fill rate and empty returns were collectively the bigger driver — I just couldn't see it because the model was dividing their signal.
>
> **R:** My manager lost confidence in that analysis, and honestly, he should have. I was presenting a conclusion I didn't fully understand the mechanics behind. That stung, but it was the right lesson at the right time. What I did about it: first, I went back, corrected the interpretation, and presented the revised findings — transparently, not quietly. I owned the mistake in the same forum where I'd made the original claim. Second, I built quality checks into every regression analysis going forward — specifically testing for multicollinearity before interpreting coefficients, and documenting my assumptions so someone could challenge them before they reached a stakeholder. Over time, the rigor I brought to subsequent analyses rebuilt that trust. But the deeper lesson was: understanding *why* a model says what it says matters as much as what it says. If you can't explain the mechanics, you're not ready to present the conclusion.

**Why this works for Extreme Ownership:** It's a genuine analytical mistake — not a humble-brag. You owned it publicly, corrected it in the same forum, and changed your process. The trust hit is what makes it credible; the recovery is what makes it impressive.

---

### 2. Executive Judgment

*"What do you think makes reporting valuable versus just informative?"*
*Tests: business impact beyond dashboards*

> Reporting is valuable when it changes a decision. Informative reporting tells you what happened — valuable reporting tells you what to do about it and what's at stake if you don't.
>
> At Hitch, I inherited a weekly business review that was informative — 120+ metrics across four departments, updated weekly. But leadership was still making decisions based on gut feel because the report didn't prioritize. I stripped it down, pushed back on vanity metrics like website traffic and app downloads, and focused on input metrics tied to our core goal of improving margins.
>
> The test I used: Is this metric actionable? Does it tie to a company goal? Is it worth the effort to maintain? If the answer to any of those was no, it didn't belong.
>
> The bigger win wasn't the automation — it was discovering that leadership was tracking one-way fill rate when the real driver was round-trip fill rate. That single metric shift helped us go from -10% margins to +20% in six months. The WBR went from a reporting obligation to the meeting that actually drove company strategy.

---

### 3. Ambiguity Handling

*"You join and realize different teams define engagement differently, but everyone seems comfortable with it. Do you fix it immediately or observe first?"*
*Tests: judgment + change management instincts*

> I observe first — but I observe actively, not passively.
>
> When I joined Planoly, conversion rates were tracked in multiple Google Sheets pulling from different sources. Marketing owned GA4, engineering owned the backend database, and the numbers didn't match. Nobody had fixed it because everyone had adapted — they'd just caveat their own numbers in meetings.
>
> I spent the first two weeks mapping what each team actually meant when they said "conversion" and where each definition lived in the systems. I didn't announce a project or call a meeting — I just asked questions and documented. Once I had the full picture, I built dbt models in BigQuery that calculated metrics at each funnel stage with clear, testable definitions. Then I created a dashboard and walked each team through it — not as "your numbers were wrong," but as "here's one source of truth we can all reference."
>
> The reason I don't fix immediately: you don't know what you don't know yet, and premature standardization can break things people depend on. But I also don't wait indefinitely — I set a personal deadline of two weeks to map the landscape, then I act. Observation without a timeline is just avoidance.

---

### 4. AI Philosophy

*"BetterUp is AI-forward. Where do you think AI should not be used in analytics?"*
*Tests: maturity + governance thinking*

> AI shouldn't be used where errors are invisible and stakes are high.
>
> In analytics, that means the narrative layer — the part where you interpret what the data means for a specific audience and make a recommendation. AI can draft a summary, surface anomalies, auto-populate templates. But deciding whether a metric shift is real risk versus normal variation, or framing a recommendation for a CFO who's skeptical about a program — that requires context, judgment, and stakeholder awareness that AI doesn't have.
>
> The danger isn't that AI will be wrong — it's that it'll be wrong in a way that's plausible enough that nobody catches it. A hallucinated trend in a partner-facing report can erode trust faster than no report at all.
>
> Where I've found AI most valuable: compressing the assembly layer. At Hitch, the manual work was pulling data from six sources into a PowerPoint. That's exactly what AI and automation should handle — the plumbing, the formatting, the first pass. Free up the human for the work that actually moves the needle: judgment, storytelling, and knowing what to leave out.
>
> I think the principle is: AI should make the analyst faster, not replace the analyst's thinking.

---

### 5. Executive Communication

*"How do you decide what not to show in an executive report?"*
*Tests: signal vs. noise discipline*

> I use a filter: does this data point help the executive make the decision they're here to make? If not, it doesn't belong — regardless of how interesting it is or how much work went into it.
>
> At Hitch, our WBR kept growing because every department wanted their metrics represented. At one point, leadership asked for website traffic and app downloads. I pushed back — those are vanity metrics. You can't act on them, they don't tie to margins, and including them trains the executive team to skim instead of focus.
>
> The harder version of this: leaving off data that's real but distracting. At Planoly, I found a segmentation filter bug that was duplicating prospects in one of our marketing dashboards. I reported the bug and the fix to the relevant stakeholders, but I didn't put the bug itself in the executive report — I put the corrected numbers. The executive team needed to trust the dashboard, not debug it. The operational detail went into a separate reference doc.
>
> My rule: the executive gets the "so what," not the "how I got there." The methodology lives in documentation for anyone who wants to validate.

---

### 6. Tradeoff Thinking

*"If you had to choose between faster reporting or more accurate reporting, what would you optimize for?"*
*Tests: business judgment*

> It depends on the decision timeline and the cost of being wrong.
>
> For a weekly operational review — faster. The goal of a WBR is to catch directional shifts early enough to act. If I spend three days perfecting a report and the issue I could have flagged on day one already caused damage, accuracy didn't help. When I automated Hitch's WBR, I explicitly accepted a small margin of error in exchange for speed — the Python script would occasionally round differently than a manual calculation, but the directional insights were always sound, and the team got them every Monday morning instead of Thursday.
>
> For a partner-facing renewal report — accuracy, without question. If a CFO sees a number that doesn't reconcile with their internal data, you've lost credibility for the entire presentation. Speed doesn't matter if the audience doesn't trust the numbers.
>
> The real answer is: build your system so you don't have to choose. Automation gives you speed. Data quality checks and validation layers give you accuracy. Invest upfront in the pipeline so that both are possible — that's what I did with the WBR, and that's the approach I'd take at scale.

---

### 7. Culture & Impact — Why BetterUp?

*"Why BetterUp? Why this role instead of continuing in marketplace analytics?"*
*Tests: intentionality*

> Three reasons, and they're specific to BetterUp — not generic "mission-driven company" answers.
>
> First, the problem is genuinely interesting to me. Partner analytics at BetterUp is the intersection of data, human behavior, and business outcomes. You're not just tracking clicks — you're measuring whether coaching actually changes how people show up at work. That's a fundamentally different kind of analytics question, and it requires more judgment and nuance than anything I've done in marketplace or e-commerce analytics.
>
> Second, the role matches exactly where I want to grow. I've spent the last few years as a sole analyst building from scratch — intake systems, WBRs, forecasting models, the whole stack. I'm proud of that, but I want to do it within a team. I want an analytics manager I can learn from, peers to collaborate with, and an organization that takes the analytics function seriously enough to invest in it. BetterUp is building that function, and this role is part of that build.
>
> Third, I actually believe in coaching. I practice yoga and meditation. I've experienced firsthand how intentional self-development changes your decision-making and resilience. BetterUp is applying that at scale with real data behind it, and that resonates with me personally — not just professionally.

---

### 8. Systems Thinking

*"If you could redesign the analytics function from scratch here, what would you focus on first?"*
*Tests: vision + architecture thinking*

> The data ecosystem — specifically, a single source of truth that every downstream report pulls from.
>
> At every company I've joined, the first problem is the same: data lives in five different places, three different people calculate the same metric three different ways, and nobody fully trusts any single number. Everything downstream — dashboards, reports, executive summaries — inherits that fragmentation.
>
> So step one is mapping every data source, understanding what each system is actually tracking, and building a governed transformation layer — dbt models, a data dictionary, tested metric definitions. That's not glamorous, but it's the foundation. Without it, you're building dashboards on sand.
>
> Step two is templating. Once the data is reliable, you standardize the delivery mechanism — a repeatable BVR template, automated data assembly, threshold-based flagging. This is what lets you scale from 5 partners to 50 without linearly scaling headcount.
>
> Step three is intelligence. Once the plumbing and templates are solid, you layer in anomaly detection, trend surfacing, and AI-assisted narrative drafts. But only after the foundation is trustworthy — because AI on bad data just produces confident-sounding garbage faster.
>
> Foundation → Standardization → Intelligence. In that order.

---

### 9. Conflict Handling

*"Tell me about a time a stakeholder disagreed with your recommendation."*
*Tests: influence without authority*

**Use: Ghost Trips (same story, different angle — here emphasize the influence arc)**

> **S:** At Hitch, heading into a supply-constrained period, our COO and I recommended using ghost trips — pre-scheduling empty outbound legs so drivers could pick up passengers on the return. Our CEO disagreed. He was concerned about two specific things: margins with an always-empty outbound, and driver reliability without passengers on the first leg.
>
> **T:** I respected his judgment — he'd been running the business for years — so we didn't push forward. But I didn't drop it. I decided to let the data settle the debate.
>
> **A:** After the constrained period passed, I ran a controlled comparison. I pulled data on ghost trips versus the last 5 accepted regular trips during supply-constrained windows — the trips where we'd had to offer large bonuses just to get a driver to accept. I compared margins and on-time performance. I didn't frame it as "proving the CEO wrong" — I framed it as "testing our assumptions so we make a better decision next time."
>
> **R:** The data showed margins were essentially identical, but ghost trips had dramatically better on-time performance — almost always on time versus 30 minutes late on average. I presented this in the WBR, led with the data, and let the numbers do the persuading. The CEO came around, and we integrated ghost trips into our strategy for supply-constrained cities. The key was: I didn't argue in the moment. I gathered evidence, presented it objectively, and let the stakeholder arrive at the conclusion themselves.

---

**Alternative story: Google ROI Metric (lighter, faster — for a follow-up or shorter version)**

> At a previous role, a stakeholder asked me to verify a marketing spend ROI metric. I found an error, quick fix. But then they wanted a major overhaul of the ROI calculation logic — outside scope. I communicated three things: the time cost, the marginal impact (we were already cutting Google spend and ROI was negative either way), and that I had higher-impact work tied to our main company goal. I created a ticket so it wouldn't get lost, proposed prioritizing it next cycle, and asked if that worked. The stakeholder understood. The key was being transparent about trade-offs without being dismissive of their ask.

---

## Additional Likely Questions by Theme

### Extreme Ownership Questions

**"Tell me about a time something failed and it was your fault."**

Use: Planoly segmentation bug

> **S:** At Planoly, I built a new feature into our conversion funnel dashboard that filtered between new and repeat prospects. After it went live, the marketing VP messaged me that free trial sign-ups looked unusually low.
>
> **T:** Numbers were about 3 standard deviations below the mean — something was clearly wrong. My first instinct was to check my own pipeline.
>
> **A:** I traced the pipeline from report back to source (Stripe). The data matched — so the pipeline was fine. But then I remembered: I had personally tried to sign up for a trial the day before and hit a checkout error. I connected the dots — something in the recent release had broken checkout. I immediately messaged the VPs with the bug, what it was, and the estimated revenue impact. Within an hour we had a hotfix deployed. Then I pulled a list of everyone who hit the checkout page during the bug window and suggested we send a recovery email with a 30% discount. Within another hour, the email went out and 15% of affected users converted.
>
> **R:** We recovered quickly because I treated it as my problem — even though the checkout bug wasn't my code. The lesson I took: if you're the person closest to the data, you're the first line of defense regardless of whose code broke. I now build monitoring alerts for any metric that's more than 2 standard deviations from baseline.

---

**"Tell me about a time you went beyond your job description."**

Use: WBR at Hitch

> **S:** When I joined Hitch as the senior data analyst, the WBR wasn't my responsibility — four people across Ops, Engineering, Marketing, and CS were each spending about 10 hours a week pulling metrics into a shared PowerPoint.
>
> **T:** Nobody asked me to fix it. But I saw 40 hours of company time per week going to a process that could be automated, and the output still wasn't driving good decisions because the metrics were scattered and unfocused.
>
> **A:** I met with each person, mapped their sources and calculations, consolidated everything into our data warehouse, built dbt models, and wrote a Python script to auto-generate the visualizations. But the bigger ownership move was pushing back on what went into the report. I fought to remove vanity metrics, introduced an intake process for new metric requests, and redirected the conversation toward input metrics like round-trip fill rate that actually tied to our goals.
>
> **R:** 40 hours down to 1 hour, $73K/year saved. But the real outcome was that the WBR became the meeting that drove company strategy — leadership pivoted goals around fill rate, and margins went from -10% to +20% in six months. That happened because I didn't just automate the existing process — I owned what the process should be.

---

### Craftsperson Questions

**"What does quality mean to you in your work?"**

> Quality means the person downstream — whether that's a CEO, a partner, or an offshore analyst — can trust the output without having to verify it themselves.
>
> Practically, that shows up in three ways. First, data accuracy: I build tests into my dbt models, I validate against source systems, and I document metric definitions so there's no ambiguity. Second, communication clarity: every number I present has context — benchmarks, trend direction, and a "so what." A metric without context is just a number. Third, repeatability: if I build something, another analyst should be able to maintain it. That means clean code, documentation, and a clear separation between data transformation and presentation.
>
> The thing I'm most proud of on the quality front: at Hitch, when our Snowflake costs doubled overnight, I didn't just find the problem — I broke down costs by user, traced individual queries, identified two unused services (Hightouch and an Intercom connector), and got them shut off. The result was costs 64% *below* baseline. I could have stopped at "costs are back to normal." But the craftsperson in me wanted to understand the full picture — and that extra digging saved an additional $2,400/month.

---

**"Tell me about a time you improved a process that was 'good enough.'"**

Use: WBR metric curation

> **S:** At Hitch, the WBR was automated and running smoothly — my automation had already saved 40 hours a week. Most people would have called it done.
>
> **T:** But I noticed the report was growing. Every week, an exec would ask for a new metric, and it was easier to add than to say no. We were creeping toward a junk drawer.
>
> **A:** I implemented a three-question filter for any new metric request: Is it actionable? Does it tie to a company goal? Is it worth the maintenance cost? I also built a Linear board to track requests so leadership could see the queue and understand prioritization decisions. When they asked for website traffic and app downloads, I pushed back with that framework — interesting data, but not decision-driving data.
>
> **R:** The WBR stayed focused, and the discipline of curating metrics — not just adding them — is what led us to discover round-trip fill rate as the real driver. That metric wouldn't have stood out in a report with 150 metrics. It stood out because the report had 20.

---

### Builder Questions

**"Tell me about something you built from scratch."**

Use: Demand Forecasting Model at Hitch

> **S:** At Hitch, heading into the 2024 holiday season, the company had no way to predict demand spikes. When they hit, it was chaos — we'd either cancel rides or pay drivers double to show up last-minute, which destroyed margins.
>
> **T:** I was tasked with building something — anything — that could give operations even a few days of lead time.
>
> **A:** I started with regression and ML approaches because that's what my training said to do. The accuracy was terrible — sparse, highly variable historical data meant too much variance. So I simplified radically. I built a SQL-based model using just two variables: days out from departure and average bookings at that point in the booking window. More biased but dramatically more reliable — and critically, easy for stakeholders to understand and trust. I surfaced it in a dashboard, set up Slack alerts for ops and support, and worked with engineering to integrate dynamic pricing that updated daily based on the forecast.
>
> **R:** The model let us do proactive marketing to drivers before high-demand periods, increasing supply without last-minute premiums. Between better pricing and lower payouts, it added about $63K/year in net revenue. The builder lesson: sometimes the best thing you can build is the simplest version that actually works. I could have spent months perfecting an ML model that nobody trusted. Instead I shipped something useful in weeks.

---

**"Tell me about a time you had to figure something out with no playbook."**

Use: Snowflake Cost Investigation

> **S:** At Hitch, our Snowflake costs doubled overnight. There was no monitoring in place, no cost allocation framework, and nobody had dealt with this before. It was just me and the data warehouse.
>
> **T:** I needed to diagnose what happened, fix it, and make sure it didn't happen again.
>
> **A:** I started with a time-series analysis to find the exact date and approximate time the cost jumped. Since Snowflake costs have very low day-to-day variance, the inflection point was clear. My first hypothesis was a recent Fivetran bug — I made changes, but the next day costs were unchanged. So I went deeper: broke down the time series by Snowflake user. Two users accounted for 95% of the cost increase. One was "Hightouch" — a reverse ETL tool that our engineer confirmed was no longer in production use. Easy fix: disabled it. The other was "Fivetran," which ran many services. I drilled into individual queries, found the highest-cost ones were from Intercom (our support tool). Talked to the support lead — they weren't using any of the data Snowflake was providing to Intercom. Got engineering to shut off that connector.
>
> **R:** Costs dropped 64% *below* our pre-spike baseline, saving $2,400/month ongoing. There was no playbook — I just kept asking "why" and peeling back layers until I found the root causes. I also built cost monitoring alerts afterward so we'd catch the next anomaly in hours, not days.

---

**"Describe a time you created a system or process where none existed."**

Use: Analytics Intake System

> **S:** At Hitch, I was the sole analyst receiving 10–20 analytics requests per week from across the company — product, ops, marketing, CS, executives — with no formal intake process. Requests came via Slack DMs, email, hallway conversations. Things were getting dropped.
>
> **T:** I needed to create a system that made the request flow transparent, prioritized, and sustainable.
>
> **A:** I designed a structured intake form that required stakeholders to articulate three things before I'd accept a request: the urgency, the specific business question, and the intended action or outcome. This filter alone eliminated poorly scoped requests before they consumed any resources. I integrated submissions with Slack alerts for visibility and tied them to our Linear backlog for tracking. For each request, I'd do a quick scoping call to clarify requirements and align on deliverables — requiring mutual sign-off before work began. Then I prioritized with my manager using an impact-versus-capacity framework: high-urgency, high-impact work pulled into the current sprint; everything else was sequenced transparently.
>
> **R:** Scope creep dropped significantly, nothing fell through the cracks, and stakeholders could see where their request sat in the queue and why. The bigger outcome was trust: people stopped escalating through back channels because the system was transparent. And it freed me to focus on the high-impact work instead of constantly context-switching between DMs.

---

## Quick Reference: Story → Theme Mapping


| Story                                | Extreme Owner | Craftsperson | Builder | Best For                                                   |
| ------------------------------------ | ------------- | ------------ | ------- | ---------------------------------------------------------- |
| WBR Automation (Hitch)               | X             | X            | X       | Going beyond role, quality curation, building from scratch |
| Regression Multicollinearity (Hitch) | X             | X            |         | Owning analytical mistakes, rigor, trust recovery          |
| Ghost Trips Analysis (Hitch)         | X             |              |         | Conflict handling, data-driven influence                   |
| Demand Forecasting (Hitch)           |               | X            | X       | Building 0→1, simplifying, craftsmanship in modeling       |
| Snowflake Cost Investigation (Hitch) | X             | X            |         | Ownership of ambiguous problems, relentless debugging      |
| Funnel/CRO (Planoly)                 |               | X            | X       | Ambiguity handling, building systems, data quality         |
| Trial Sign-Up Bug (Planoly)          | X             |              |         | Extreme ownership, speed, cross-functional action          |
| Google ROI Pushback                  | X             |              |         | Stakeholder conflict, prioritization                       |
| Analytics Intake System (Hitch)      |               |              | X       | Process creation, scaling                                  |
| Round-Trip Fill Rate (Hitch)         |               | X            |         | Finding the right metric, executive judgment               |


---

## Interviewer-Specific Notes

### Jason Moon (Extreme Owner & Craftsperson)

- **Staff engineer for 25+ years** — he's seen a lot of people. Don't oversell. Be precise and honest.
- **jQuery contributor** — he values open-source mindset, giving back, quality standards. If relevant, mention how you document and share your work.
- **Frontend background** — he'll appreciate clean, testable systems thinking even in analytics context. Talk about dbt tests, data validation, pipeline reliability.
- **He's been at BetterUp 5+ years** — he deeply understands the culture. Be authentic about why BetterUp, not generic.
- **Likely vibe:** Technical, detail-oriented, values humility and ownership. Don't bluff.

### Hunter Black (Builder)

- **Organizational psychologist, 10+ years at BetterUp** — he studies these competencies professionally. He'll notice your self-awareness, growth mindset, and how you reflect on your own behavior.
- **Coaching science expert** — the meta-layer matters. How you talk about learning from mistakes, iterating, and growing is as important as the story itself.
- **Very early BetterUp employee** — he's seen the company go from early stage to scale. Builder stories about going from 0→1 will resonate strongly.
- **Likely vibe:** Warm, psychologically attuned, will probe for depth and self-reflection. Don't just tell the story — tell what it taught you.

---

## Delivery Reminders

- **These are conversational.** Kush said they're looser than technical rounds. Don't sound rehearsed — sound like you're telling a colleague about your work.
- **Pause and let them follow up.** Don't try to cover everything in one answer. Leave room for them to dig in.
- **Show self-awareness.** When you describe a win, acknowledge what was hard or what you'd do differently. This is especially important with Hunter.
- **Use "I" not "we."** These interviews want to know what YOU did. It's fine to acknowledge the team, but be specific about your contribution.
- **Restate the question.** Even a quick "So you're asking about a time I..." shows you're listening and buying yourself a second to organize.
- **Name the measurable outcome.** Every story should end with a number: $73K saved, -10% to +20% margins, 64% cost reduction, $555K/year revenue, 15% conversion lift.
- **Invite follow-up.** End with "Happy to go deeper on any part of that" — it signals confidence and keeps the conversation flowing.
- **Don't force BetterUp references.** These are about your past work. The connection to BetterUp happens naturally through your values and approach, not by name-dropping the company.

---

## If You Have Time for Questions at the End

They said time may be limited, but have 1–2 ready:

**For Jason (Extreme Owner & Craftsperson):**

- "What does extreme ownership look like day-to-day on the engineering/product side at BetterUp? I'd love to understand how that shows up across functions."
- "What's something about BetterUp's culture that surprised you after joining?"

**For Hunter (Builder):**

- "You've been at BetterUp for over 10 years — what's changed the most about the builder mindset as the company has scaled?"
- "How does the coaching science team's research influence how the company thinks about its own internal culture?"

