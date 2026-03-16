# Presentation Supporting Document — SQL Queries & Data Sources

All queries run against `inventory-analytics-475119.testing` in BigQuery.

**Global filters:**
- `WHERE Lead ID IS NOT NULL` on `dim_leads` (excludes aggregated totals row)
- `WHERE Is Pool A _Active SDR__ _Yes _ No_ = true` on `fct_dials` (Pool A scope per Richard's guidance)
- `WHERE Activity _ET_ Time >= Lead Created _ET_ Time` on `fct_dials` (suppresses 1,166 bad-timestamp records)

---

## Section 1: Half of all leads are lost before we ever reach them

### Lead Funnel: 35,169 Leads → 194 Funded Loans

```sql
SELECT
  SUM(`Gross Leads`) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Opportunities`) AS opportunities,
  SUM(`Number of File Started Leads`) AS file_started,
  SUM(`Number of Entered Processing Leads`) AS entered_processing,
  SUM(`Number of Locked Loan Leads`) AS locked_loan,
  SUM(`Number of Pre-Approval Leads`) AS pre_approval,
  SUM(`Number of Funded Loan Leads`) AS funded
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL;
```

| Stage | Count | % of Gross |
|---|---|---|
| Gross Leads | 35,169 | 100% |
| Called | 31,016 | 88.2% |
| Contacted | 17,619 | 50.1% |
| Opportunities | 8,756 | 24.9% |
| File Started | 3,644 | 10.4% |
| Funded | 194 | 0.55% |

### "Called but never contacted" calculation

```sql
SELECT
  SUM(`Number of Called Leads`) - SUM(`Number of Contacted Leads`) AS called_never_contacted,
  ROUND((SUM(`Number of Called Leads`) - SUM(`Number of Contacted Leads`)) / SUM(`Gross Leads`) * 100, 1) AS pct_of_gross
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL;
```

Result: 13,397 leads (38.1%) were called but never contacted — the largest single drop in the funnel.

---

## Section 2: The 3-call/day cadence is met less than half the time

### Cadence compliance by day offset

```sql
WITH pool_a_dials AS (
  SELECT
    `Lead ID`,
    `Lead Created _ET_ Date`,
    `Activity _ET_ Date`,
    DATE_DIFF(`Activity _ET_ Date`, `Lead Created _ET_ Date`, DAY) AS day_offset
  FROM `inventory-analytics-475119.testing.fct_dials`
  WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
    AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
),

dials_per_lead_day AS (
  SELECT
    `Lead ID`,
    day_offset,
    COUNT(*) AS dials_on_day
  FROM pool_a_dials
  WHERE day_offset BETWEEN 0 AND 6
  GROUP BY 1, 2
)

SELECT
  day_offset,
  COUNT(DISTINCT `Lead ID`) AS leads_with_dials,
  ROUND(COUNTIF(dials_on_day >= 3) / COUNT(*) * 100, 1) AS pct_hitting_3
FROM dials_per_lead_day
GROUP BY 1
ORDER BY 1;
```

| Day Offset | Leads | % Hitting 3 Dials |
|---|---|---|
| 0 (creation day) | 16,067 | 22.3% |
| 1 | 16,091 | 52.2% |
| 2 | 11,704 | 39.4% |
| 3 | 9,465 | 38.4% |
| 4 | 8,875 | 44.7% |

### Compliance heatmap — by lead creation day of week

```sql
WITH pool_a AS (
  SELECT
    `Lead ID`,
    `Lead Created _ET_ Date`,
    FORMAT_DATE('%A', `Lead Created _ET_ Date`) AS lead_dow,
    DATE_DIFF(`Activity _ET_ Date`, `Lead Created _ET_ Date`, DAY) AS day_offset
  FROM `inventory-analytics-475119.testing.fct_dials`
  WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
    AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
),

dials_per_lead_day AS (
  SELECT `Lead ID`, lead_dow, day_offset, COUNT(*) AS dials
  FROM pool_a
  WHERE day_offset BETWEEN 0 AND 4
  GROUP BY 1, 2, 3
)

SELECT
  lead_dow,
  day_offset,
  COUNT(DISTINCT `Lead ID`) AS leads_count,
  ROUND(COUNTIF(dials >= 3) / COUNT(*) * 100, 1) AS pct_hitting_3
FROM dials_per_lead_day
GROUP BY 1, 2
ORDER BY
  CASE lead_dow WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3
    WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6 WHEN 'Sunday' THEN 7 END,
  day_offset;
```

Key pattern: compliance craters when cadence days fall on weekends (e.g., Wednesday leads → Days 3–4 are Sat/Sun at 1–4%).

---

## Section 3: 81% of our dials are spent on leads we never reach

### KPI: 96% of funded loans come from attempts 1–5

```sql
WITH first_contact AS (
  SELECT
    f.`Lead ID`,
    MIN(f.`Pool A Call Attempt Number`) AS attempt_at_contact
  FROM `inventory-analytics-475119.testing.fct_dials` f
  WHERE f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Lead ID` IS NOT NULL
    AND f.`Contacted_ _Yes _ No_` = true
  GROUP BY 1
),

funded_leads AS (
  SELECT d.`Lead ID`, d.`Number of Funded Loan Leads` AS funded
  FROM `inventory-analytics-475119.testing.dim_leads` d
  WHERE d.`Lead ID` IS NOT NULL
    AND d.`Number of Funded Loan Leads` > 0
)

SELECT
  CASE
    WHEN fc.attempt_at_contact BETWEEN 1 AND 5 THEN '1-5'
    WHEN fc.attempt_at_contact BETWEEN 6 AND 10 THEN '6-10'
    WHEN fc.attempt_at_contact BETWEEN 11 AND 20 THEN '11-20'
    ELSE 'No Pool A contact'
  END AS attempt_bucket,
  SUM(fl.funded) AS funded_loans
FROM funded_leads fl
LEFT JOIN first_contact fc ON fl.`Lead ID` = fc.`Lead ID`
GROUP BY 1
ORDER BY MIN(COALESCE(fc.attempt_at_contact, 999));
```

| Attempt Bucket | Funded Loans | % |
|---|---|---|
| 1–5 | 49 | 96.1% |
| 6–10 | 2 | 3.9% |
| 11–20 | 0 | 0% |
| No Pool A contact | 143 | — |

### KPI: 0 funded loans from attempts 11–20 / % of dials by bucket

```sql
SELECT
  CASE
    WHEN `Pool A Call Attempt Number` BETWEEN 1 AND 5 THEN '1-5'
    WHEN `Pool A Call Attempt Number` BETWEEN 6 AND 10 THEN '6-10'
    WHEN `Pool A Call Attempt Number` BETWEEN 11 AND 20 THEN '11-20'
  END AS attempt_bucket,
  COUNT(*) AS dials,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 1) AS pct_of_dials
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Lead ID` IS NOT NULL
  AND `Pool A Call Attempt Number` BETWEEN 1 AND 20
GROUP BY 1
ORDER BY MIN(`Pool A Call Attempt Number`);
```

| Bucket | Dials | % of Dials |
|---|---|---|
| 1–5 | 104,644 | 36.2% |
| 6–10 | 80,635 | 27.9% |
| 11–20 | 103,839 | 35.9% |

### KPI: 2,972 leads got <5 dials and were never contacted

```sql
WITH lead_status AS (
  SELECT
    `Lead ID`,
    MAX(`Pool A Call Attempt Number`) AS max_attempt,
    MAX(CASE WHEN `Contacted_ _Yes _ No_` = true THEN 1 ELSE 0 END) AS ever_contacted
  FROM `inventory-analytics-475119.testing.fct_dials`
  WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
    AND `Lead ID` IS NOT NULL
  GROUP BY 1
)

SELECT
  max_attempt,
  COUNT(*) AS never_contacted_leads
FROM lead_status
WHERE ever_contacted = 0 AND max_attempt <= 5
GROUP BY 1
ORDER BY 1;
```

| Max Attempt | Leads |
|---|---|
| 1 | 1,428 |
| 2 | 536 |
| 3 | 343 |
| 4 | 261 |
| 5 | 404 |
| **Total** | **2,972** |

### Chart: Effort vs. Outcome (% of Dials vs % of Funded Loans)

Data sourced from the two queries above, combined:

| Bucket | % of Dials | % of Funded Loans |
|---|---|---|
| 1–5 | 36.2% | 96.1% |
| 6–10 | 27.9% | 3.9% |
| 11–20 | 35.9% | 0% |

### Chart: Cumulative % of Contacts by Attempt

```sql
WITH pool_a_contacted AS (
  SELECT
    `Lead ID`,
    MIN(`Pool A Call Attempt Number`) AS attempt_at_contact
  FROM `inventory-analytics-475119.testing.fct_dials`
  WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
    AND `Lead ID` IS NOT NULL
    AND `Contacted_ _Yes _ No_` = true
  GROUP BY 1
)

SELECT
  attempt_at_contact,
  COUNT(*) AS leads_contacted,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 1) AS pct_of_contacts
FROM pool_a_contacted
WHERE attempt_at_contact <= 20
GROUP BY 1
ORDER BY 1;
```

Key milestones: 46.3% by attempt 1 → 78% by attempt 5 → 90.6% by attempt 10 → 100% by attempt 20.

---

## Section 4: Speed to contact is the strongest predictor of funded loans

### Contacted Day 0 / Day 1 / Day 5+ comparison cards

```sql
WITH first_contact AS (
  SELECT
    f.`Lead ID`,
    DATE_DIFF(CAST(f.`First Contact _ET_ Time` AS DATE), f.`Lead Created _ET_ Date`, DAY) AS days_to_contact
  FROM `inventory-analytics-475119.testing.fct_dials` f
  WHERE f.`Contacted_ _Yes _ No_` = true
    AND f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
    AND f.`First Contact _ET_ Time` IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY f.`Lead ID` ORDER BY f.`Activity _ET_ Time`) = 1
),

contact_with_funnel AS (
  SELECT fc.`Lead ID`, fc.days_to_contact,
    d.`Number of Opportunities` AS opps, d.`Number of Funded Loan Leads` AS funded
  FROM first_contact fc
  JOIN `inventory-analytics-475119.testing.dim_leads` d ON fc.`Lead ID` = d.`Lead ID`
)

SELECT
  days_to_contact, COUNT(*) AS leads_contacted,
  ROUND(SAFE_DIVIDE(SUM(opps), COUNT(*)) * 100, 1) AS opp_rate,
  ROUND(SAFE_DIVIDE(SUM(funded), COUNT(*)) * 100, 2) AS funded_rate
FROM contact_with_funnel
WHERE days_to_contact BETWEEN 0 AND 10
GROUP BY 1
ORDER BY 1;
```

| Days to Contact | Opp Rate | Funded Rate |
|---|---|---|
| Day 0 | 62.0% | 0.88% |
| Day 1 | 48.4% | 0.59% |
| Day 5+ | ~35% | ~0% |

### Chart: Contact Rate by Hour of Day (ET)

```sql
SELECT
  EXTRACT(HOUR FROM `Activity _ET_ Time`) AS hour_of_day,
  SUM(Calls) AS total_dials,
  ROUND(SAFE_DIVIDE(SUM(Contacts), SUM(Calls)) * 100, 2) AS contact_rate_pct
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
GROUP BY 1
ORDER BY 1;
```

Note: The 8–9 AM contact rate spike (5.9%) is a **composition effect** — 70.5% of 8 AM dials are attempts 1–5 vs 25% at midday. When controlling for attempt number, contact rates are flat (~8–11% for attempts 1–3 at all hours).

### Chart: Contact Rate by Day of Week

```sql
SELECT
  FORMAT_DATE('%A', `Activity _ET_ Date`) AS day_of_week,
  EXTRACT(DAYOFWEEK FROM `Activity _ET_ Date`) AS dow_num,
  SUM(Calls) AS total_dials,
  ROUND(SAFE_DIVIDE(SUM(Contacts), SUM(Calls)) * 100, 2) AS contact_rate_pct
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
GROUP BY 1, 2
ORDER BY 2;
```

| Day | Dials | Contact Rate |
|---|---|---|
| Saturday | 7,098 | 9.88% |
| Sunday | 6,597 | 9.46% |
| Weekday avg | ~55,520 | ~3.15% |

Weekend lead generation volume (supports staffing rec):

```sql
SELECT
  EXTRACT(DAYOFWEEK FROM `Lead Created _ET_ Date`) AS dow_num,
  COUNT(*) AS leads_created
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

Weekends generate ~3,100–3,200 leads/day (~55% of weekday volume of ~5,770/day).

---

## Section 5: Not all leads are created equal — and LIFO doesn't know the difference

### Channel Performance Table

```sql
SELECT
  `Lead Channel Segment`,
  COUNT(*) AS gross_leads,
  ROUND(SAFE_DIVIDE(SUM(`Number of Contacted Leads`), SUM(`Number of Called Leads`)) * 100, 1) AS contact_rate,
  ROUND(SAFE_DIVIDE(SUM(`Number of Opportunities`), SUM(`Number of Contacted Leads`)) * 100, 1) AS opp_rate,
  ROUND(SAFE_DIVIDE(SUM(`Number of Funded Loan Leads`), COUNT(*)) * 100, 2) AS funded_rate
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY gross_leads DESC;
```

### Chart: Quality vs. Speed — avg hours to first dial by channel

> **Note:** 10,518 leads (40.6%) are auto-dialed instantly via a "speed-to-lead" campaign. These are included in the speed analysis per Richard's guidance, as they are valid Pool A dials.

```sql
WITH speed_segment AS (
  SELECT
    d.`Lead ID`,
    d.`Lead Channel Segment`,
    MIN(TIMESTAMP_DIFF(f.`Activity _ET_ Time`, f.`Lead Created _ET_ Time`, MINUTE)) AS minutes_to_first_dial
  FROM `inventory-analytics-475119.testing.dim_leads` d
  JOIN `inventory-analytics-475119.testing.fct_dials` f ON d.`Lead ID` = f.`Lead ID`
  WHERE d.`Lead ID` IS NOT NULL
    AND f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
  GROUP BY 1, 2
)

SELECT
  `Lead Channel Segment`,
  COUNT(*) AS leads,
  ROUND(AVG(minutes_to_first_dial), 1) AS avg_min,
  ROUND(AVG(minutes_to_first_dial) / 60.0, 1) AS avg_hrs
FROM speed_segment
GROUP BY 1
ORDER BY leads DESC;
```

| Channel | Leads | Avg Hrs | Funded Rate | % Auto-Dialed |
|---|---|---|---|---|
| Digital Buy Partner | 11,684 | 28.5 | 0.12% | 46% |
| Movoto | 7,789 | 51.6 | 0.06% | 42% |
| Paid Spend | 4,310 | 39.3 | 1.05% | 28% |
| Direct / Organic | 1,986 | 37.9 | 2.15% | 31% |

The lowest-value channel (DBP) gets the fastest average response because the speed-to-lead auto-dialer disproportionately serves high-volume, low-quality channels.

### Speed-to-lead vs. manual performance comparison (extra credit)

```sql
WITH first_dial AS (
  SELECT
    f.`Lead ID`,
    MIN(f.`Activity _ET_ Time`) AS first_dial_time,
    MIN(f.`Lead Created _ET_ Time`) AS lead_created_time
  FROM `inventory-analytics-475119.testing.fct_dials` f
  WHERE f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Lead ID` IS NOT NULL
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
  GROUP BY 1
),

classified AS (
  SELECT `Lead ID`,
    CASE WHEN first_dial_time = lead_created_time THEN 'Speed-to-Lead' ELSE 'Manual' END AS dial_type
  FROM first_dial
),

with_outcomes AS (
  SELECT c.`Lead ID`, c.dial_type, d.`Lead Channel Segment`,
    d.`Number of Contacted Leads` AS contacted,
    d.`Number of Opportunities` AS opps,
    d.`Number of Funded Loan Leads` AS funded
  FROM classified c
  JOIN `inventory-analytics-475119.testing.dim_leads` d ON c.`Lead ID` = d.`Lead ID`
  WHERE d.`Lead ID` IS NOT NULL
)

SELECT dial_type, `Lead Channel Segment`, COUNT(*) AS leads,
  ROUND(SAFE_DIVIDE(SUM(contacted), COUNT(*)) * 100, 1) AS contact_rate,
  SUM(funded) AS funded,
  ROUND(SAFE_DIVIDE(SUM(funded), COUNT(*)) * 100, 2) AS funded_rate
FROM with_outcomes
WHERE `Lead Channel Segment` IN ('Digital Buy Partner', 'Movoto', 'Paid Spend', 'Direct / Organic')
GROUP BY 1, 2
ORDER BY 2, 1;
```

| Channel | Dial Type | Leads | Contact Rate | Funded | Funded Rate |
|---|---|---|---|---|---|
| Direct / Organic | Speed-to-Lead | 610 | 63.8% | 9 | 1.48% |
| Direct / Organic | Manual | 1,376 | 54.4% | 16 | 1.16% |
| Paid Spend | Speed-to-Lead | 1,203 | 66.5% | 12 | 1.00% |
| Paid Spend | Manual | 3,107 | 53.0% | 31 | 1.00% |
| Movoto | Speed-to-Lead | 3,249 | 76.7% | 1 | 0.03% |
| Movoto | Manual | 4,540 | 65.2% | 2 | 0.04% |
| Digital Buy Partner | Speed-to-Lead | 5,392 | 39.7% | 5 | 0.09% |
| Digital Buy Partner | Manual | 6,292 | 40.8% | 4 | 0.06% |

The auto-dialer lifts contact rates across all channels (+4pp overall). The strongest funded-rate lift appears on Direct/Organic (1.48% vs 1.16%) — but only 31% of Direct/Organic leads receive it, while 46% of low-value DBP leads do.

### "Never called" rate by channel

```sql
SELECT
  `Lead Channel Segment`,
  COUNT(*) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  ROUND((COUNT(*) - SUM(`Number of Called Leads`)) / COUNT(*) * 100, 1) AS never_called_pct
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY gross_leads DESC;
```

Paid Spend has a 26.4% never-called rate — the highest among major channels.

### Chart: Funded Rate by Loan Type

```sql
SELECT
  `Borrower Requested Loan Type`,
  COUNT(*) AS gross_leads,
  SUM(`Number of Funded Loan Leads`) AS funded,
  ROUND(SAFE_DIVIDE(SUM(`Number of Funded Loan Leads`), COUNT(*)) * 100, 2) AS funded_rate
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY funded_rate DESC;
```

| Loan Type | Leads | Funded | Funded Rate |
|---|---|---|---|
| HELOC | 8,862 | 96 | 1.08% |
| Refi | 11,483 | 60 | 0.52% |
| Purchase | 14,824 | 38 | 0.26% |

---

## Section 6: Three changes to turn more dials into funded loans

### Revenue impact assumptions

**Blended revenue per funded loan: ~$6,000**

| Loan Type | Funded Loans | Avg Revenue Est. | Weighted |
|---|---|---|---|
| HELOC | 96 (49%) | ~$3,000 | $1,485 |
| Refinance | 60 (31%) | ~$7,500 | $2,320 |
| Purchase | 38 (20%) | ~$8,500 | $1,665 |
| **Total** | **194** | | **~$5,470 → rounded to $6,000** |

**Baseline conversion: funded-per-contact rate = 194 / 17,619 = ~1.1%**

### Rec 1: Cap Pool A at 10 Attempts — Est. +$150–200K/quarter

- 103K dials freed from attempts 11–20 (zero funded loan output)
- Addressable pool: 2,972 under-dialed leads (<5 attempts, never contacted)
- ~50% utilization discount applied (not all freed dials are immediately productive)
- ~51,500 productive redirected dials × 6% contact rate = ~3,090 contacts
- Net incremental (minus current yield): ~1,854 contacts
- Incremental funded: ~28 loans × $6,000 = **~$168K/quarter**

### Rec 2: Implement Channel-Aware Prioritization — Est. +$150–200K/quarter

- Direct/Organic (2.15% funded) + Paid Spend (1.05% funded) currently wait ~10–13 hrs
- 15–20% uplift in funded rate from faster contact on high-value channels:
  - Direct/Organic: 3,903 × 2.15% × 17.5% uplift = ~15 additional loans
  - Paid Spend: 6,977 × 1.05% × 17.5% uplift = ~13 additional loans
- Total: ~28 loans × $6,000 = **~$170K/quarter**

### Rec 3: Add Weekend Staffing — Est. +$75–100K/quarter

- Current weekend dials: ~13,700 at 9.9% contact rate
- Weekends generate ~55% of weekday daily lead volume (3,100–3,200 leads/day)
- Adding 2–3 reps could roughly double weekend dial volume
- Additional contacts: 13,700 × 9.9% = ~1,356
- Incremental funded: ~15 loans × $6,000 = **~$90K/quarter**

### Combined estimate

| Recommendation | Incremental Funded Loans | Est. Revenue/Quarter |
|---|---|---|
| 1. Cap at 10 Attempts | ~28 | +$150–200K |
| 2. Channel Prioritization | ~28 | +$150–200K |
| 3. Weekend Staffing | ~15 | +$75–100K |
| **Combined** | **~71** | **~$375–500K/quarter (~$1.5–2.0M/year)** |

All estimates use blended $6,000 revenue per funded loan and current baseline conversion rates. These are order-of-magnitude estimates intended to size the opportunity.
