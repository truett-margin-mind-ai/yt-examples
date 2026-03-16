# Storytelling with Data — Best Practices & Key Insights

Summary of *Storytelling with Data: A Data Visualization Guide for Business Professionals* by Cole Nussbaumer Knaflic.

---

## The Core Premise

Technology makes creating graphs easy. But few people can use data to tell a clear, compelling story that drives action. The book provides a six-step framework for transforming data from a collection of numbers into a persuasive narrative.

---

## The Six Steps

### Step 1: Understand the Context

Before touching any tool or chart, answer three questions:

- **Who** is your audience? What do they care about? What's their relationship to you?
- **What** do you want them to know or do? What action should result from this communication?
- **How** will data support your case? What's the right mechanism (live presentation, email, report)?

Then distill your message:

- **The Big Idea** — A single sentence that captures your core message. It must contain (1) a unique point of view, (2) stakes (why it matters), and (3) a proposed action. If you can't write this sentence, you aren't ready to build a visual.
- **The 3-Minute Story** — Force yourself to tell the entire narrative in three minutes. This strips away everything non-essential and ensures you know what actually matters.
- **Storyboard first** — Use Post-it notes or a whiteboard to plan the structure and flow of your communication *before* opening any software. Rearrange until the logic is airtight.

**Critical distinction:** Exploratory analysis is what you do to find insights. Explanatory analysis is what you present. Never show all your exploratory work — the audience only needs the "so what."

---

### Step 2: Choose an Effective Visual

You can handle the vast majority of business communication needs with a small set of chart types:

| Visual Type | When to Use |
|---|---|
| **Simple text** | When you have 1-2 numbers to communicate. A big, bold number with context is more powerful than a chart. |
| **Table** | When your audience needs to look up specific values, or when different audiences need different data from the same view. |
| **Heatmap** | A table enhanced with color saturation to layer in visual patterns while preserving exact values. |
| **Line chart** | For continuous data, especially trends over time. The line itself carries meaning — it implies continuity between points. |
| **Bar chart** | The workhorse. Use for categorical comparisons. Horizontal bars are often better than vertical for readability (especially with long category names). |
| **Stacked bar** | For part-to-whole comparisons. 100% stacked horizontal bars are a strong pie chart alternative. |
| **Scatterplot** | To show the relationship between two variables. |
| **Slopegraph** | To emphasize change between two time periods or categories. |

**What to avoid:**

- **Pie charts** — Human eyes are bad at comparing angles and areas. A bar chart almost always communicates the same information more clearly. If you must use one, limit to 2-3 slices max.
- **3D effects** — They distort perception of values and add zero informational value.
- **Secondary y-axes** — They confuse more than they help. Use separate charts instead.
- **Donut charts** — Same problems as pie charts, with less data-ink.

**Rules for bar charts:**
- Always start the y-axis at zero — truncating the baseline distorts relative comparisons.
- Use consistent bar widths.
- Order bars intentionally (by value, or by a natural order like time).

---

### Step 3: Eliminate Clutter

Every element on your visual adds cognitive load. Clutter is anything that takes up space without adding information.

#### Gestalt Principles of Visual Perception

These describe how humans subconsciously organize what they see. Use them intentionally:

| Principle | Description | Application |
|---|---|---|
| **Proximity** | Elements close together are perceived as related | Group related data points; separate unrelated ones with whitespace |
| **Similarity** | Elements that look alike are grouped together | Use consistent colors/shapes for related categories |
| **Enclosure** | Elements inside a border are seen as a unit | Use subtle shading (not heavy borders) to group sections |
| **Closure** | We perceive incomplete shapes as complete | You don't need full chart borders — the brain fills in gaps |
| **Continuity** | Eyes follow smooth lines and paths | Align elements to create clean reading paths |
| **Connection** | Elements linked by lines are perceived as related | Use lines to tie data to labels or annotations |

#### What to remove:

- Chart borders and backgrounds
- Gridlines (or make them very light gray)
- Unnecessary axis labels or tick marks
- Data markers on every point (unless needed for precision)
- Legends (label data directly when possible)
- Bolding, italics, or underlining used without purpose
- Any decorative element that doesn't convey data

#### The data-ink ratio

Borrowed from Edward Tufte: maximize the share of ink devoted to data vs. non-data elements. Every pixel should earn its place. White backgrounds maximize this ratio.

---

### Step 4: Focus Your Audience's Attention

Use **preattentive attributes** — visual properties the brain processes automatically, before conscious thought — to direct attention where it matters.

The three most powerful preattentive attributes:

| Attribute | How to Use It |
|---|---|
| **Color** | The strongest tool. Use it sparingly and strategically. |
| **Size** | Larger elements are perceived as more important. |
| **Position** | Western audiences scan top-left to bottom-right. Place the most important information where eyes land first. |

#### The strategic use of color

This is arguably the most important decision in any visualization:

1. **Start gray.** Push everything to the background in light gray.
2. **Apply color only where you want attention.** One bold color on the thing that matters most.
3. **Use color sparingly.** When everything is colored, nothing stands out. When one thing is colored, it commands the room.
4. **Color carries meaning.** Red = bad/alert, green = good/go. Don't fight cultural conventions.
5. **Be consistent.** Same color = same thing throughout your entire presentation.
6. **Design for colorblindness.** ~8% of men have some form of color vision deficiency. Use color + another attribute (bold, pattern) as a backup.

#### The "Where Are Your Eyes Drawn?" test

Look away from your visualization, then glance back. Where do your eyes land first? If it's not the most important element, redesign.

#### Three types of memory relevant to data visualization:

- **Iconic memory** — Ultra-fast, pre-conscious. This is where preattentive attributes work.
- **Short-term memory** — Limited to ~4 chunks of information at once. Don't overload a single visual.
- **Long-term memory** — Where stories live. Narrative structure moves information from short-term to long-term memory.

---

### Step 5: Think Like a Designer

You don't need to be a designer. You need to understand four concepts:

**Affordances** — Visual cues that signal how to interact with or read the information. Tie related elements together visually. Push secondary information to the background. Make the "entry point" of your visual obvious.

**Accessibility** — Design for the broadest possible audience. Beyond colorblindness: consider font sizes for projected presentations, label clarity for printed reports, and whether your visual makes sense without your verbal explanation.

**Aesthetics** — Beautiful things get more attention and patience from audiences. Aesthetic quality comes from ruthless editing — many small refinements (alignment, spacing, font consistency) combine into either a polished or sloppy impression. People judge credibility partly on visual quality.

**Acceptance** — A design must be accepted by its audience to be effective. Consider their expectations, comfort level, and context. An audience unfamiliar with scatterplots may reject an otherwise excellent visualization. Know when to push boundaries and when to use familiar formats.

#### Practical design tips:

- **Alignment matters.** Align text, axes, and labels to a consistent grid. Misalignment looks sloppy.
- **White space is your friend.** Don't cram. Let elements breathe.
- **Use no more than 2-3 fonts/sizes.** Establish a clear hierarchy: title, subtitle, body, annotation.
- **Sketch with pen and paper first.** It's faster to iterate on a napkin than in Excel.

---

### Step 6: Tell a Story

Stories are how humans have communicated since the beginning. They capture attention, evoke emotion, and stick in long-term memory. Data without narrative is forgettable. Data within a story is persuasive.

#### The narrative arc

Structure your data presentation like a story:

| Component | What It Does | In a Data Presentation |
|---|---|---|
| **Beginning / Setup** | Establishes context, introduces the setting | "Here's what we're looking at and why it matters" |
| **Middle / Conflict** | Introduces tension, builds the problem | "Here's what the data reveals — there's a problem / opportunity" |
| **End / Resolution** | Resolves the tension, delivers the payoff | "Here's what we should do about it — the call to action" |

The expanded narrative arc (Freytag's Pyramid):
- **Plot** — The context
- **Inciting Incident** — Where tension is introduced
- **Rising Action** — Tension builds through evidence and analysis
- **Climax** — The pivotal finding or turning point
- **Falling Action & Resolution** — Recommendation and call to action

#### Storytelling techniques:

- **Repetition** — Repeat your core message. State it at the beginning, reinforce it through the middle, and restate it at the end. Audiences need to hear something multiple times for it to stick.
- **Vertical and horizontal logic** — Vertically, each slide's title should read as a standalone narrative when strung together. Horizontally, each slide should make complete sense on its own.
- **Action titles** — Slide titles should be conclusions, not descriptions. Not "Q4 Sales by Region" but "Southeast outperformed all regions by 23% in Q4."
- **Spoken vs. written narratives** — Live presentations should have sparse slides (you are the narrator). Written reports need more detail on the page because the visual must stand alone.
- **The power of tension** — Don't lead with the answer. Build toward it. Give the audience the context and problem first so the solution feels earned.
- **Annotations > legends** — Label things directly on the chart. Don't make your audience go back and forth between a legend and the data.

---

## Seven Guiding Principles (Knaflic's personal rules)

1. **Audience trumps all else** — Every design decision flows from who is receiving the information.
2. **Words make a graph accessible** — Title your graphs and axes. Explain acronyms. Add data sources. The visual should be understandable without you standing next to it.
3. **Make it clear where to look** — Use preattentive attributes to create a visual hierarchy.
4. **Get rid of the non-essential** — Perfection is achieved not when there's nothing left to add, but when there's nothing left to remove.
5. **Don't overcomplicate** — Present complex information accessibly. Simplify, but don't oversimplify.
6. **Think like a designer** — Balance form and function. Aesthetics build credibility.
7. **Tell a story** — Data within a narrative is exponentially more powerful than data alone.

---

## Quick-Reference Checklist

Use this before finalizing any data visualization or presentation:

- [ ] Can I state my Big Idea in one sentence?
- [ ] Do I know exactly what action I want from my audience?
- [ ] Am I showing explanatory analysis (not exploratory)?
- [ ] Is the chart type the simplest one that works?
- [ ] Does the y-axis start at zero (for bar charts)?
- [ ] Have I eliminated all non-data ink I can?
- [ ] Are gridlines, borders, and backgrounds removed or minimized?
- [ ] Is color used sparingly — gray base, strategic highlight?
- [ ] Does the "where are your eyes drawn?" test pass?
- [ ] Are elements labeled directly (not via a separate legend)?
- [ ] Do slide titles state conclusions (action titles)?
- [ ] Does the presentation follow a narrative arc (setup → conflict → resolution)?
- [ ] Could someone understand this visual without me explaining it?
- [ ] Would I want to spend time looking at this?
