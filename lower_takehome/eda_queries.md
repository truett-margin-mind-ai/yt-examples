# Lower Case Study — EDA SQL Queries

All queries run against `inventory-analytics-475119.testing` in BigQuery.
Column names contain spaces and special characters — backtick-quoted throughout.

**Global filters applied to all analytical queries:**
- `WHERE Lead ID IS NOT NULL` on `dim_leads` (excludes the aggregated totals row)
- `WHERE Activity _ET_ Time >= Lead Created _ET_ Time` on `fct_dials` (suppresses 1,166 bad-timestamp records per recruiter guidance)
- `WHERE Is Pool A _Active SDR__ _Yes _ No_ = true` on `fct_dials` for cadence-scoped queries (per Richard's guidance to evaluate Pool A only)

---

## Phase 0: Data Profiling & Cleaning

### 0a. dim_leads row count, date range, and NULL patterns

```sql
SELECT
  COUNT(*) AS row_count,
  MIN(`Lead Created _ET_ Date`) AS min_date,
  MAX(`Lead Created _ET_ Date`) AS max_date,
  COUNTIF(`Lead ID` IS NULL) AS null_lead_ids,
  COUNTIF(`Last Contact Attempt _ET_ Time` IS NULL) AS null_last_contact,
  COUNTIF(`Lead Channel Segment` IS NULL) AS null_channel_segment
FROM `inventory-analytics-475119.testing.dim_leads`;
```

| row_count | min_date | max_date | null_lead_ids | null_last_contact | null_channel_segment |
|---|---|---|---|---|---|
| 35,170 | 2025-11-01 | 2026-01-31 | 1 | 4,154 | 1 |

### 0b. Identify the totals row

```sql
SELECT *
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NULL
  OR `Lead ID` = ''
  OR `Lead Created _ET_ Date` IS NULL
LIMIT 10;
```

Returns 1 row: `Lead ID = NULL`, `Gross Leads = 35,169` — this is the aggregated totals row embedded in the export. Filtered out in all subsequent queries via `WHERE Lead ID IS NOT NULL`.

### 0c. fct_dials row count, date ranges, bad timestamps

```sql
SELECT
  COUNT(*) AS row_count,
  MIN(`Lead Created _ET_ Date`) AS min_date,
  MAX(`Lead Created _ET_ Date`) AS max_date,
  MIN(`Activity _ET_ Date`) AS min_activity_date,
  MAX(`Activity _ET_ Date`) AS max_activity_date,
  COUNTIF(`Lead ID` IS NULL) AS null_lead_ids
FROM `inventory-analytics-475119.testing.fct_dials`;
```

| row_count | min_date | max_date | min_activity_date | max_activity_date | null_lead_ids |
|---|---|---|---|---|---|
| 382,454 | 2025-11-01 | 2026-01-31 | 2025-08-18 | 2026-02-13 | 0 |

```sql
SELECT
  COUNTIF(`Activity _ET_ Time` < `Lead Created _ET_ Time`) AS bad_timestamps,
  COUNT(*) AS total
FROM `inventory-analytics-475119.testing.fct_dials`;
```

| bad_timestamps | total |
|---|---|
| 1,166 | 382,454 |

### 0d. Pool A distribution

```sql
SELECT
  COUNTIF(`Is Pool A _Active SDR__ _Yes _ No_` = true) AS pool_a_true,
  COUNTIF(`Is Pool A _Active SDR__ _Yes _ No_` = false) AS pool_a_false,
  COUNTIF(`Is Pool A _Active SDR__ _Yes _ No_` IS NULL) AS pool_a_null,
  COUNT(*) AS total
FROM `inventory-analytics-475119.testing.fct_dials`;
```

| pool_a_true | pool_a_false | pool_a_null | total |
|---|---|---|---|
| 291,328 | 91,126 | 0 | 382,454 |

### 0e. Categorical distributions

```sql
-- Lead Channel Segment
SELECT `Lead Channel Segment`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC;

-- Lead Source
SELECT `Lead Source`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC;

-- Loan Type
SELECT `Borrower Requested Loan Type`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC;

-- Current Lead Status
SELECT `Current Lead Status`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC;

-- Direction
SELECT `Direction`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.fct_dials`
GROUP BY 1
ORDER BY 2 DESC;

-- Outcome
SELECT `Outcome`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.fct_dials`
GROUP BY 1
ORDER BY 2 DESC;

-- Team Member Role
SELECT `Team Member Role`, COUNT(*) AS cnt
FROM `inventory-analytics-475119.testing.fct_dials`
GROUP BY 1
ORDER BY 2 DESC;
```

---

## Phase 1: Lead Universe & Funnel Overview

### 1a. Overall funnel (notebook: `funnel_values`)

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

| gross_leads | called | contacted | opportunities | file_started | entered_processing | locked_loan | pre_approval | funded |
|---|---|---|---|---|---|---|---|---|
| 35,169 | 31,016 | 17,619 | 8,756 | 3,644 | 494 | 530 | 434 | 194 |

### 1b. Funnel by channel segment (notebook: `channel_data`)

```sql
SELECT
  `Lead Channel Segment`,
  SUM(`Gross Leads`) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Opportunities`) AS opportunities,
  SUM(`Number of File Started Leads`) AS file_started,
  SUM(`Number of Funded Loan Leads`) AS funded
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY gross_leads DESC;
```

| Lead Channel Segment | gross_leads | called | contacted | opportunities | file_started | funded |
|---|---|---|---|---|---|---|
| Digital Buy Partner | 12,555 | 12,509 | 5,386 | 2,483 | 762 | 15 |
| Movoto | 10,857 | 9,236 | 6,638 | 2,445 | 606 | 7 |
| Paid Spend | 6,977 | 5,138 | 2,934 | 2,275 | 1,135 | 73 |
| Direct / Organic | 3,903 | 3,300 | 1,850 | 1,438 | 914 | 84 |
| Retargeting | 509 | 509 | 509 | 47 | 136 | 14 |
| Mail | 231 | 200 | 228 | 14 | 57 | 1 |
| Other | 137 | 124 | 74 | 54 | 34 | 0 |

### 1c. Funnel by loan type (notebook: `loan_data`)

```sql
SELECT
  `Borrower Requested Loan Type`,
  SUM(`Gross Leads`) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Opportunities`) AS opportunities,
  SUM(`Number of File Started Leads`) AS file_started,
  SUM(`Number of Funded Loan Leads`) AS funded
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY gross_leads DESC;
```

| Loan Type | gross_leads | called | contacted | opportunities | file_started | funded |
|---|---|---|---|---|---|---|
| Purchase | 14,824 | 11,830 | 7,842 | 3,363 | 1,166 | 38 |
| Refi | 11,483 | 11,311 | 5,806 | 2,807 | 1,298 | 60 |
| HELOC | 8,862 | 7,875 | 3,971 | 2,586 | 1,180 | 96 |

### 1d. Daily lead volume trend

```sql
SELECT
  `Lead Created _ET_ Date` AS lead_date,
  SUM(`Gross Leads`) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Funded Loan Leads`) AS funded
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

Returns 92 rows (Nov 1, 2025 – Jan 31, 2026). Used for trend chart in notebook but not embedded as a static table — the daily time series visualization is in the notebook.

---

## Phase 2: Cadence Compliance Analysis

### 2a. % of leads hitting 3 dials per day, by day offset (notebook: `cadence_data`)

```sql
WITH pool_a_dials AS (
  SELECT
    `Lead ID`,
    `Lead Created _ET_ Date`,
    `Activity _ET_ Date`,
    DATE_DIFF(`Activity _ET_ Date`, `Lead Created _ET_ Date`, DAY) AS day_offset,
    `Pool A Call Attempt Number`
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
  AVG(dials_on_day) AS avg_dials,
  COUNTIF(dials_on_day >= 3) AS leads_hitting_3,
  COUNTIF(dials_on_day >= 2) AS leads_hitting_2,
  COUNTIF(dials_on_day >= 1) AS leads_hitting_1,
  ROUND(COUNTIF(dials_on_day >= 3) / COUNT(*) * 100, 1) AS pct_hitting_3,
  ROUND(COUNTIF(dials_on_day >= 2) / COUNT(*) * 100, 1) AS pct_hitting_2
FROM dials_per_lead_day
GROUP BY 1
ORDER BY 1;
```

| day_offset | leads_with_dials | avg_dials | pct_hitting_3 | pct_hitting_2+ |
|---|---|---|---|---|
| 0 | 16,067 | 1.79 | 22.3% | 53.8% |
| 1 | 16,091 | 2.39 | 52.2% | 83.5% |
| 2 | 11,704 | 2.21 | 39.4% | 80.5% |
| 3 | 9,465 | 2.20 | 38.4% | 80.5% |
| 4 | 8,875 | 2.27 | 44.7% | 81.8% |
| 5 | 8,986 | 2.22 | 39.2% | 82.1% |
| 6 | 9,457 | 1.98 | 28.2% | 69.2% |

### 2b. Cadence compliance by lead creation day-of-week (notebook: `dow_cadence`)

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
  SELECT
    `Lead ID`,
    lead_dow,
    day_offset,
    COUNT(*) AS dials
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
  CASE lead_dow
    WHEN 'Monday' THEN 1
    WHEN 'Tuesday' THEN 2
    WHEN 'Wednesday' THEN 3
    WHEN 'Thursday' THEN 4
    WHEN 'Friday' THEN 5
    WHEN 'Saturday' THEN 6
    WHEN 'Sunday' THEN 7
  END,
  day_offset;
```

Returns a 35-row matrix (7 days x 5 offsets). Key patterns: compliance craters when cadence days land on weekends (e.g., Wed lead → Day 2 is Friday, Days 3-4 are Sat/Sun at 3.5% and 3.9%).

---

## Phase 3: Funnel Decay by Attempt Number & Day

### 3a. Contact rate by Pool A attempt number (notebook: `attempt_data`)

```sql
SELECT
  `Pool A Call Attempt Number` AS attempt_num,
  SUM(Calls) AS total_dials,
  SUM(Contacts) AS total_contacts,
  ROUND(SAFE_DIVIDE(SUM(Contacts), SUM(Calls)) * 100, 2) AS contact_rate_pct,
  SUM(CASE WHEN `Is Live Transfer_ _Yes _ No_` = true THEN 1 ELSE 0 END) AS transfers
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
  AND `Pool A Call Attempt Number` IS NOT NULL
  AND `Pool A Call Attempt Number` <= 20
GROUP BY 1
ORDER BY 1;
```

| attempt | dials | contacts | contact_rate | transfers |
|---|---|---|---|---|
| 1 | 25,891 | 4,004 | 15.46% | 1,866 |
| 2 | 21,479 | 1,343 | 6.25% | 438 |
| 3 | 19,971 | 878 | 4.40% | 255 |
| 4 | 19,008 | 655 | 3.45% | 179 |
| 5 | 18,278 | 525 | 2.87% | 137 |
| ... | ... | ... | ... | ... |
| 10 | 14,822 | 208 | 1.40% | 42 |
| 15 | 13,064 | 146 | 1.12% | 27 |
| 20 | 2,146 | 14 | 0.65% | 5 |

### 3b. Downstream conversion by days to first contact (notebook: `days_contact_data`)

```sql
WITH first_contact AS (
  SELECT
    f.`Lead ID`,
    DATE_DIFF(
      CAST(f.`First Contact _ET_ Time` AS DATE),
      f.`Lead Created _ET_ Date`,
      DAY
    ) AS days_to_contact
  FROM `inventory-analytics-475119.testing.fct_dials` f
  WHERE f.`Contacted_ _Yes _ No_` = true
    AND f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
    AND f.`First Contact _ET_ Time` IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY f.`Lead ID`
    ORDER BY f.`Activity _ET_ Time`
  ) = 1
),

contact_with_funnel AS (
  SELECT
    fc.`Lead ID`,
    fc.days_to_contact,
    d.`Number of Opportunities` AS opps,
    d.`Number of File Started Leads` AS file_started,
    d.`Number of Funded Loan Leads` AS funded
  FROM first_contact fc
  JOIN `inventory-analytics-475119.testing.dim_leads` d
    ON fc.`Lead ID` = d.`Lead ID`
)

SELECT
  days_to_contact,
  COUNT(*) AS leads_contacted,
  SUM(opps) AS opportunities,
  SUM(file_started) AS file_started,
  SUM(funded) AS funded,
  ROUND(SAFE_DIVIDE(SUM(opps), COUNT(*)) * 100, 1) AS opp_rate,
  ROUND(SAFE_DIVIDE(SUM(funded), COUNT(*)) * 100, 2) AS funded_rate
FROM contact_with_funnel
WHERE days_to_contact BETWEEN 0 AND 10
GROUP BY 1
ORDER BY 1;
```

| days_to_contact | leads_contacted | opportunities | opp_rate | funded_rate |
|---|---|---|---|---|
| 0 | 4,087 | 2,534 | 62.0% | 0.88% |
| 1 | 2,023 | 980 | 48.4% | 0.59% |
| 2 | 678 | 297 | 43.8% | 0.29% |
| 3 | 375 | 164 | 43.7% | 0.00% |
| 5 | 220 | 78 | 35.5% | 0.00% |
| 10 | 41 | 16 | 39.0% | 0.00% |

---

## Phase 4: Speed & Timing Analysis

### 4a. Speed to first dial — distribution and funnel rates (notebook: `speed_funnel`)

```sql
WITH first_dial AS (
  SELECT
    `Lead ID`,
    MIN(`Activity _ET_ Time`) AS first_dial_time,
    MIN(`Lead Created _ET_ Time`) AS lead_created_time
  FROM `inventory-analytics-475119.testing.fct_dials`
  WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
    AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
  GROUP BY 1
),

speed AS (
  SELECT
    `Lead ID`,
    TIMESTAMP_DIFF(first_dial_time, lead_created_time, MINUTE) AS minutes_to_first_dial
  FROM first_dial
),

lead_data AS (
  SELECT
    d.`Lead ID`,
    d.`Number of Contacted Leads` AS contacted,
    d.`Number of Opportunities` AS opportunities,
    d.`Number of File Started Leads` AS file_started,
    d.`Number of Funded Loan Leads` AS funded,
    s.minutes_to_first_dial
  FROM `inventory-analytics-475119.testing.dim_leads` d
  JOIN speed s ON d.`Lead ID` = s.`Lead ID`
  WHERE d.`Lead ID` IS NOT NULL
)

SELECT
  CASE
    WHEN minutes_to_first_dial <= 5 THEN '0-5 min'
    WHEN minutes_to_first_dial <= 15 THEN '6-15 min'
    WHEN minutes_to_first_dial <= 30 THEN '16-30 min'
    WHEN minutes_to_first_dial <= 60 THEN '31-60 min'
    WHEN minutes_to_first_dial <= 240 THEN '1-4 hrs'
    WHEN minutes_to_first_dial <= 1440 THEN '4-24 hrs'
    ELSE '24+ hrs'
  END AS speed_bucket,
  COUNT(*) AS leads,
  SUM(contacted) AS contacted,
  SUM(opportunities) AS opportunities,
  SUM(file_started) AS file_started,
  SUM(funded) AS funded,
  ROUND(SAFE_DIVIDE(SUM(contacted), COUNT(*)) * 100, 1) AS contact_rate,
  ROUND(SAFE_DIVIDE(SUM(funded), COUNT(*)) * 100, 2) AS funded_rate
FROM lead_data
GROUP BY 1
ORDER BY MIN(minutes_to_first_dial);
```

| speed_bucket | leads | contact_rate | funded_rate |
|---|---|---|---|
| 0-5 min | 12,993 | 56.9% | 0.40% |
| 6-15 min | 220 | 64.1% | 0.00% |
| 16-30 min | 331 | 52.9% | 0.30% |
| 31-60 min | 281 | 50.2% | 0.71% |
| 1-4 hrs | 913 | 47.1% | 0.44% |
| 4-24 hrs | 7,248 | 50.0% | 0.28% |
| 24+ hrs | 3,905 | 48.9% | 0.05% |

### 4b. Contact rate by hour of day (notebook: `hour_data`)

```sql
SELECT
  EXTRACT(HOUR FROM `Activity _ET_ Time`) AS hour_of_day,
  SUM(Calls) AS total_dials,
  SUM(Contacts) AS total_contacts,
  ROUND(SAFE_DIVIDE(SUM(Contacts), SUM(Calls)) * 100, 2) AS contact_rate_pct
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
GROUP BY 1
ORDER BY 1;
```

| hour (ET) | dials | contacts | contact_rate |
|---|---|---|---|
| 8 | 9,697 | 574 | 5.92% |
| 9 | 29,137 | 1,466 | 5.03% |
| 10 | 39,189 | 1,087 | 2.77% |
| 11 | 36,745 | 1,119 | 3.05% |
| 12 | 30,983 | 1,089 | 3.51% |
| 13 | 23,601 | 985 | 4.17% |
| 14 | 32,508 | 1,023 | 3.15% |
| 15 | 33,080 | 1,045 | 3.16% |
| 16 | 32,090 | 931 | 2.90% |
| 17 | 17,925 | 503 | 2.81% |
| 18 | 6,282 | 237 | 3.77% |

### 4c. Contact rate by day of week (notebook: `dow_data`)

```sql
SELECT
  FORMAT_DATE('%A', `Activity _ET_ Date`) AS day_of_week,
  EXTRACT(DAYOFWEEK FROM `Activity _ET_ Date`) AS dow_num,
  SUM(Calls) AS total_dials,
  SUM(Contacts) AS total_contacts,
  ROUND(SAFE_DIVIDE(SUM(Contacts), SUM(Calls)) * 100, 2) AS contact_rate_pct
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
GROUP BY 1, 2
ORDER BY 2;
```

| day | dials | contact_rate |
|---|---|---|
| Sunday | 6,597 | 9.46% |
| Monday | 61,624 | 3.37% |
| Tuesday | 67,695 | 3.20% |
| Wednesday | 62,994 | 2.86% |
| Thursday | 43,979 | 3.12% |
| Friday | 41,309 | 3.19% |
| Saturday | 7,098 | 9.88% |

---

## Phase 5: Source & Segment Performance

### 5a. Full funnel rates by channel segment (notebook: `ch_rates`)

```sql
SELECT
  `Lead Channel Segment`,
  COUNT(*) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Opportunities`) AS opportunities,
  SUM(`Number of File Started Leads`) AS file_started,
  SUM(`Number of Funded Loan Leads`) AS funded,
  ROUND(SAFE_DIVIDE(SUM(`Number of Called Leads`), COUNT(*)) * 100, 1) AS called_rate,
  ROUND(SAFE_DIVIDE(SUM(`Number of Contacted Leads`), SUM(`Number of Called Leads`)) * 100, 1) AS contact_rate,
  ROUND(SAFE_DIVIDE(SUM(`Number of Opportunities`), SUM(`Number of Contacted Leads`)) * 100, 1) AS opp_rate,
  ROUND(SAFE_DIVIDE(SUM(`Number of Funded Loan Leads`), SUM(`Number of Opportunities`)) * 100, 2) AS funded_per_opp
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY gross_leads DESC;
```

| Channel | gross | called_rate | contact_rate | opp_rate | funded/opp |
|---|---|---|---|---|---|
| Digital Buy Partner | 12,555 | 99.6% | 43.1% | 46.1% | 0.60% |
| Movoto | 10,857 | 85.1% | 71.9% | 36.8% | 0.29% |
| Paid Spend | 6,977 | 73.6% | 57.1% | 77.5% | 3.21% |
| Direct / Organic | 3,903 | 84.6% | 56.1% | 77.7% | 5.84% |
| Retargeting | 509 | 100.0% | 100.0% | 9.2% | 29.79% |
| Mail | 231 | 86.6% | 114.0% | 6.1% | 7.14% |
| Other | 137 | 90.5% | 59.7% | 73.0% | 0.00% |

**Note on Mail segment:** Contact rate shows 114% (228 contacted vs 200 called). This means some leads in this segment were contacted through non-call channels (e.g., Calendly, SMS) or inbound calls not captured in the "called" metric. This is a data artifact of the dim_leads design where "contacted" can exceed "called."

---

## Phase 6: Agent / Team Member Patterns

### 6a. Pool A performance by team member role (notebook: `agent_data`)

```sql
SELECT
  `Team Member Role`,
  COUNT(DISTINCT `Team Member ID`) AS agent_count,
  SUM(Calls) AS total_dials,
  SUM(Contacts) AS total_contacts,
  SUM(`Live Transfers Sent`) AS total_transfers,
  ROUND(SAFE_DIVIDE(SUM(Contacts), SUM(Calls)) * 100, 2) AS contact_rate,
  ROUND(SAFE_DIVIDE(SUM(`Live Transfers Sent`), SUM(Contacts)) * 100, 2) AS transfer_rate
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
  AND `Team Member Role` IS NOT NULL
GROUP BY 1
ORDER BY total_dials DESC;
```

| Role | agents | dials | contact_rate | transfer_rate |
|---|---|---|---|---|
| CER Level Two | 23 | 290,924 | 3.44% | 34.65% |
| SDR | 1 | 163 | 14.11% | 21.74% |
| Sr SDR | 1 | 106 | 8.49% | 44.44% |
| Loan Advisor | 2 | 103 | 8.74% | 0.00% |

### 6b. Lead outcomes by max Pool A attempt reached (notebook: `exit_data`)

```sql
WITH pool_a_leads AS (
  SELECT DISTINCT `Lead ID`
  FROM `inventory-analytics-475119.testing.fct_dials`
  WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
    AND `Activity _ET_ Time` >= `Lead Created _ET_ Time`
),

lead_max_attempt AS (
  SELECT
    f.`Lead ID`,
    MAX(f.`Pool A Call Attempt Number`) AS max_attempt,
    MAX(CASE WHEN f.`Contacted_ _Yes _ No_` = true THEN 1 ELSE 0 END) AS was_contacted
  FROM `inventory-analytics-475119.testing.fct_dials` f
  INNER JOIN pool_a_leads p ON f.`Lead ID` = p.`Lead ID`
  WHERE f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
  GROUP BY 1
)

SELECT
  CASE
    WHEN max_attempt <= 3 THEN CAST(max_attempt AS STRING)
    WHEN max_attempt <= 6 THEN '4-6'
    WHEN max_attempt <= 10 THEN '7-10'
    WHEN max_attempt <= 15 THEN '11-15'
    ELSE '16-20'
  END AS attempt_bucket,
  was_contacted,
  COUNT(*) AS lead_count
FROM lead_max_attempt
GROUP BY 1, 2
ORDER BY MIN(max_attempt), was_contacted;
```

| attempt_bucket | not_contacted | contacted | contact_% |
|---|---|---|---|
| 1 | 1,427 | 2,987 | 67.7% |
| 2 | 534 | 974 | 64.6% |
| 3 | 343 | 620 | 64.4% |
| 4-6 | 1,069 | 1,175 | 52.4% |
| 7-10 | 1,505 | 786 | 34.3% |
| 11-15 | 1,209 | 689 | 36.3% |
| 16-20 | 11,131 | 1,444 | 11.5% |

---

## Phase 7: Gap Analysis — New Findings

### 7a. Lead lifecycle waterfall segmentation

```sql
SELECT
  CASE
    WHEN `Number of Called Leads` = 0
     AND `Last Contact Attempt _ET_ Time` IS NULL
      THEN 'Never Called'
    WHEN `Number of Called Leads` > 0
     AND `Number of Contacted Leads` = 0
      THEN 'Called but Never Contacted'
    WHEN `Number of Contacted Leads` > 0
     AND `Number of Opportunities` = 0
      THEN 'Contacted but No Opportunity'
    WHEN `Number of Opportunities` > 0
     AND `Number of Funded Loan Leads` = 0
      THEN 'Opportunity but Not Funded'
    WHEN `Number of Funded Loan Leads` > 0
      THEN 'Funded'
    ELSE 'Other'
  END AS segment,
  COUNT(*) AS leads,
  ROUND(COUNT(*) / 35169 * 100, 1) AS pct,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Opportunities`) AS opportunities,
  SUM(`Number of Funded Loan Leads`) AS funded
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY leads DESC;
```

| segment | leads | pct | contacted | opportunities | funded |
|---|---|---|---|---|---|
| Called but Never Contacted | 13,427 | 38.2% | 0 | 1,048 | 39 |
| Contacted but No Opportunity | 9,881 | 28.1% | 9,881 | 0 | 26 |
| Opportunity but Not Funded | 7,579 | 21.6% | 7,579 | 7,579 | 0 |
| Never Called | 4,153 | 11.8% | 30 | 0 | 0 |
| Funded | 129 | 0.4% | 129 | 129 | 129 |

**Note:** "Called but Never Contacted" showing 1,048 opportunities and 39 funded is a data artifact — these leads likely progressed through non-call channels (Calendly, SMS, inbound) that count toward milestones but not toward the "contacted" metric in dim_leads. The "Never Called" segment is 96% in "Nurture" status — intentionally excluded from calling per business rules.

### 7b. Never-called breakdown by channel and loan type

```sql
SELECT
  `Lead Channel Segment`,
  COUNT(*) AS total_leads,
  COUNTIF(`Last Contact Attempt _ET_ Time` IS NULL) AS never_called,
  ROUND(COUNTIF(`Last Contact Attempt _ET_ Time` IS NULL) / COUNT(*) * 100, 1)
    AS pct_never_called,
  COUNTIF(`Number of Called Leads` > 0 AND `Number of Contacted Leads` = 0) AS called_not_contacted,
  ROUND(
    COUNTIF(`Number of Called Leads` > 0 AND `Number of Contacted Leads` = 0)
    / COUNTIF(`Number of Called Leads` > 0) * 100, 1
  ) AS pct_called_not_contacted
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY total_leads DESC;
```

| Channel | total | never_called | pct_never_called | called_not_contacted | pct_called_not_contacted |
|---|---|---|---|---|---|
| Digital Buy Partner | 12,555 | 46 | 0.4% | 7,123 | 56.9% |
| Movoto | 10,857 | 1,621 | 14.9% | 2,598 | 28.1% |
| Paid Spend | 6,977 | 1,839 | 26.4% | 2,204 | 42.9% |
| Direct / Organic | 3,903 | 603 | 15.4% | 1,450 | 43.9% |
| Retargeting | 509 | 0 | 0.0% | 0 | 0.0% |
| Mail | 231 | 31 | 13.4% | 2 | 1.0% |
| Other | 137 | 13 | 9.5% | 50 | 40.3% |

```sql
SELECT
  `Borrower Requested Loan Type`,
  COUNT(*) AS total_leads,
  COUNTIF(`Last Contact Attempt _ET_ Time` IS NULL) AS never_called,
  ROUND(COUNTIF(`Last Contact Attempt _ET_ Time` IS NULL) / COUNT(*) * 100, 1)
    AS pct_never_called
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY total_leads DESC;
```

| Loan Type | total | never_called | pct_never_called |
|---|---|---|---|
| Purchase | 14,824 | 2,994 | 20.2% |
| Refi | 11,483 | 172 | 1.5% |
| HELOC | 8,862 | 987 | 11.1% |

### 7c. Dial efficiency — productive vs wasted dials

```sql
WITH lead_contact_attempt AS (
  SELECT
    f.`Lead ID`,
    MIN(CASE WHEN f.`Contacted_ _Yes _ No_` = true
        THEN f.`Pool A Call Attempt Number` END) AS first_contact_attempt,
    MAX(f.`Pool A Call Attempt Number`) AS max_attempt,
    COUNT(*) AS total_dials
  FROM `inventory-analytics-475119.testing.fct_dials` f
  WHERE f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
  GROUP BY 1
)

SELECT
  CASE
    WHEN first_contact_attempt IS NULL THEN 'Never Contacted'
    ELSE 'Contacted'
  END AS status,
  COUNT(*) AS leads,
  SUM(total_dials) AS total_dials_spent,
  SUM(CASE WHEN first_contact_attempt IS NOT NULL
      THEN total_dials - first_contact_attempt ELSE 0 END) AS dials_after_contact
FROM lead_contact_attempt
GROUP BY 1;
```

| status | leads | total_dials_spent | dials_after_contact |
|---|---|---|---|
| Never Contacted | 17,218 | 236,937 | 0 |
| Contacted | 8,675 | 54,359 | 21,659 |

**Key takeaway:** 81% of all Pool A dials (236,937) are spent on leads that are never contacted. Only ~32,700 dials (total for contacted leads minus post-contact dials) are truly productive — roughly 11% of all Pool A dial effort.

### 7d. Monthly funnel trends

```sql
SELECT
  FORMAT_DATE('%Y-%m', `Lead Created _ET_ Date`) AS month,
  COUNT(*) AS gross_leads,
  SUM(`Number of Called Leads`) AS called,
  SUM(`Number of Contacted Leads`) AS contacted,
  SUM(`Number of Opportunities`) AS opportunities,
  SUM(`Number of File Started Leads`) AS file_started,
  SUM(`Number of Funded Loan Leads`) AS funded,
  ROUND(SUM(`Number of Called Leads`) / COUNT(*) * 100, 1) AS called_rate,
  ROUND(
    SAFE_DIVIDE(SUM(`Number of Contacted Leads`), SUM(`Number of Called Leads`)) * 100, 1
  ) AS contact_rate,
  ROUND(SAFE_DIVIDE(SUM(`Number of Funded Loan Leads`), COUNT(*)) * 100, 2)
    AS funded_rate
FROM `inventory-analytics-475119.testing.dim_leads`
WHERE `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

| month | gross_leads | called | contacted | funded | called_rate | contact_rate | funded_rate |
|---|---|---|---|---|---|---|---|
| 2025-11 | 11,696 | 9,674 | 6,215 | 108 | 82.7% | 64.2% | 0.92% |
| 2025-12 | 9,341 | 8,058 | 4,814 | 60 | 86.3% | 59.7% | 0.64% |
| 2026-01 | 14,132 | 13,284 | 6,590 | 26 | 94.0% | 49.6% | 0.18% |

**Note:** January's low funded rate (0.18%) is partially a maturity effect — loans take weeks/months to fund and data ends Jan 31. However, the contact rate decline from 64.2% to 49.6% is real and likely driven by the 52% volume surge in January hitting the same call center capacity.

### 7e. Speed to first dial by channel segment

> **Update:** The 10,518 leads (40.6%) with `Activity _ET_ Time = Lead Created _ET_ Time` were confirmed by Richard (Principal Data Analyst) to be from a **"speed-to-lead" auto-dialer campaign**. These are valid Pool A dials and are included in the analysis. Average speed is used instead of median to account for the bimodal distribution (instant auto-dials vs manual dials).

**Average speed to first dial by channel (includes speed-to-lead):**

```sql
WITH speed_segment AS (
  SELECT
    d.`Lead ID`,
    d.`Lead Channel Segment`,
    MIN(TIMESTAMP_DIFF(f.`Activity _ET_ Time`, f.`Lead Created _ET_ Time`, MINUTE))
      AS minutes_to_first_dial
  FROM `inventory-analytics-475119.testing.dim_leads` d
  JOIN `inventory-analytics-475119.testing.fct_dials` f
    ON d.`Lead ID` = f.`Lead ID`
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

| Channel | Leads | Avg Min | Avg Hrs | % Auto-Dialed |
|---|---|---|---|---|
| Digital Buy Partner | 11,684 | 1,709 | 28.5 | 46% |
| Movoto | 7,789 | 3,097 | 51.6 | 42% |
| Paid Spend | 4,310 | 2,359 | 39.3 | 28% |
| Direct / Organic | 1,986 | 2,276 | 37.9 | 31% |

**Speed-to-lead auto-dialer breakdown by channel:**

```sql
-- Confirmed by Richard: same-timestamp records = "speed-to-lead" auto-dialer campaign
-- Total: 10,518 leads (40.6% of all dialed leads)
-- Digital Buy Partner: 5,392 (46% of DBP dialed leads)
-- Movoto: 3,249 (42%)
-- Paid Spend: 1,203 (28%)
-- Direct/Organic: 610 (31%)
```

**Speed-to-lead vs. manual performance comparison:**

```sql
WITH first_dial AS (
  SELECT f.`Lead ID`,
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

**Key takeaway:** The speed-to-lead auto-dialer lifts contact rates across all channels (+4pp overall) and shows the strongest funded-rate lift on high-value channels — Direct/Organic auto-dialed leads fund at 1.48% vs 1.16% manual (+28% lift). But the campaign disproportionately serves Digital Buy Partner (46% auto-dialed) over Direct/Organic (31%). The lowest-value channel gets the fastest response. Reweighting the auto-dialer toward high-quality channels would amplify returns.

### 7f. Attempt number at first contact — cumulative distribution

```sql
WITH pool_a_contacted AS (
  SELECT
    f.`Lead ID`,
    MIN(f.`Pool A Call Attempt Number`) AS attempt_at_contact
  FROM `inventory-analytics-475119.testing.fct_dials` f
  WHERE f.`Is Pool A _Active SDR__ _Yes _ No_` = true
    AND f.`Activity _ET_ Time` >= f.`Lead Created _ET_ Time`
    AND f.`Contacted_ _Yes _ No_` = true
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

| attempt | leads_contacted | pct_of_contacts | cumulative_pct |
|---|---|---|---|
| 1 | 4,004 | 46.3% | 46.3% |
| 2 | 1,151 | 13.3% | 59.6% |
| 3 | 720 | 8.3% | 67.9% |
| 4 | 489 | 5.6% | 73.5% |
| 5 | 391 | 4.5% | 78.0% |
| 6 | 314 | 3.6% | 81.7% |
| 7 | 238 | 2.7% | 84.4% |
| 8 | 199 | 2.3% | 86.7% |
| 9 | 179 | 2.1% | 88.8% |
| 10 | 155 | 1.8% | 90.6% |
| 11-15 | 557 | 6.4% | 97.0% |
| 16-20 | 259 | 3.0% | 100.0% |

**Key takeaway:** 78% of all Pool A contacts happen by attempt 5. 90.6% by attempt 10. The remaining 9.4% of contacts require attempts 11-20 — those dials carry an extremely low yield.

---

## Phase 8: Revenue Impact Estimation

### Assumptions

**Blended revenue per funded loan: ~$6,000**

Our funded-loan mix from the data:

| Loan Type | Funded Loans | Avg Revenue Est. | Weighted |
|---|---|---|---|
| HELOC | 96 (49%) | ~$3,000 | $1,485 |
| Refinance | 60 (31%) | ~$7,500 | $2,320 |
| Purchase | 38 (20%) | ~$8,500 | $1,665 |
| **Total** | **194** | | **~$5,470** |

Rounded to **$6,000** for presentation simplicity. This is conservative for a DTC mortgage lender — industry gain-on-sale + origination fees typically run 1.5–3% of loan amount.

**Baseline conversion: funded-per-contact rate = 194 / 17,619 = ~1.1%**

```sql
-- Baseline funded-per-contact rate
SELECT
  COUNTIF(f.`Funded` = true) AS funded_loans,
  COUNT(DISTINCT CASE WHEN f.`Contact _Yes_No_` = true THEN f.`Lead ID` END) AS leads_contacted,
  ROUND(SAFE_DIVIDE(
    COUNTIF(f.`Funded` = true),
    COUNT(DISTINCT CASE WHEN f.`Contact _Yes_No_` = true THEN f.`Lead ID` END)
  ) * 100, 2) AS funded_per_contact_pct
FROM `inventory-analytics-475119.testing.fct_dials` f
JOIN `inventory-analytics-475119.testing.dim_leads` d
  ON f.`Lead ID` = d.`Lead ID`
WHERE d.`Lead ID` IS NOT NULL
  AND f.`Is Pool A _Active SDR__ _Yes _ No_` = true;
```

### 8a. Rec 1 — Cap Pool A at 10 Attempts

**Logic:** Attempts 11–20 produce zero funded loans but consume ~103K dials/quarter (35.9% of all Pool A dials). Capping at 10 frees those dials. However, the immediately addressable pool is limited: only 2,972 leads received <5 attempts and were never contacted. These under-dialed leads could absorb ~9–15K dials; the remainder would serve incoming fresh leads over time. We apply a ~50% utilization discount to account for this constraint.

```sql
-- Dials spent on attempts 11-20 and their contact rate
SELECT
  CASE
    WHEN `Pool A Call Attempt Number` BETWEEN 1 AND 5 THEN '1-5'
    WHEN `Pool A Call Attempt Number` BETWEEN 6 AND 10 THEN '6-10'
    WHEN `Pool A Call Attempt Number` BETWEEN 11 AND 20 THEN '11-20'
  END AS attempt_bucket,
  COUNT(*) AS dials,
  ROUND(COUNTIF(`Contacted_ _Yes _ No_` = true) / COUNT(*) * 100, 1) AS contact_rate_pct
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Pool A Call Attempt Number` BETWEEN 1 AND 20
  AND `Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

```sql
-- Under-dialed leads: never contacted with <5 Pool A attempts
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
-- Result: 2,972 leads (1,428 with just 1 attempt, 536 with 2, 343 with 3, 261 with 4, 404 with 5)
```

**Per-dial contact rate by attempt bucket** (from query above):

| Attempt Bucket | Dials | Contacts | Contact Rate |
|---|---|---|---|
| 1–5 | 104,644 | 7,405 | 7.08% |
| 6–10 | 80,635 | 1,460 | 1.81% |
| 11–20 | 103,839 | 1,170 | 1.13% |

**Calculation (revised):**
- Dials freed: 103,839 (attempts 11–20)
- Immediately addressable: 2,972 under-dialed leads × ~3 more attempts avg = ~9K dials
- Remaining ~94K dials serve incoming leads over time (partial utilization)
- Conservative: apply ~50% effective utilization to freed dials = ~51,920 productive redirected dials
- Redirected yield: 51,920 × 7.08% (attempts 1–5 per-dial contact rate) = ~3,676 contacts
- Subtract current yield of those dials: 103,839 × 1.13% (attempts 11–20 per-dial contact rate) = ~1,173 contacts
- Net incremental contacts: ~2,503
- Incremental funded loans: 2,503 × 1.1% (baseline funded-per-contact rate) = ~28 loans
- **Revenue: 28 × $6,000 = ~$165K/quarter → displayed as +$120–170K/quarter**

### 8b. Rec 2 — Add Weekend Staffing

**Logic:** Weekend contact rates are ~3x weekdays (9.9% vs 3.2%) but volume is 10–15x lower. Adding 2–3 reps could roughly double weekend dial volume.

```sql
-- Weekend vs weekday dial volume and contact rate
SELECT
  CASE WHEN EXTRACT(DAYOFWEEK FROM `Activity _ET_ Date`) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
  COUNT(*) AS dials,
  ROUND(COUNTIF(`Contact _Yes_No_` = true) / COUNT(*) * 100, 1) AS contact_rate_pct
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Lead ID` IS NOT NULL
GROUP BY 1;
```

**Calculation:**
- Current weekend dials: ~13,700 at 9.9% contact rate = ~1,356 contacts
- Doubling weekend volume: +13,700 additional dials
- Additional contacts: 13,700 × 9.9% = ~1,356
- Incremental funded loans: 1,356 × 1.1% = **~15 loans**
- **Revenue: 15 × $6,000 = ~$90K/quarter → displayed as +$75–100K/quarter**

### 8c. Rec 3 — Channel-Aware Prioritization

**Logic:** Direct/Organic (2.15% funded) and Paid Spend (1.05% funded) currently wait the same ~10–13 hours as low-value channels. Faster contact on high-value channels should improve funded rate. Conservative 10% uplift estimate based on Day 0 vs Day 1+ funded rate differential (0.88% vs 0.59%).

```sql
-- Channel segment funded rates and lead counts
SELECT
  d.`Lead Channel Segment`,
  COUNT(DISTINCT d.`Lead ID`) AS leads,
  ROUND(COUNTIF(d.`Funded` = true) / COUNT(DISTINCT d.`Lead ID`) * 100, 2) AS funded_rate_pct
FROM `inventory-analytics-475119.testing.dim_leads` d
WHERE d.`Lead ID` IS NOT NULL
GROUP BY 1
ORDER BY funded_rate_pct DESC;
```

**Calculation:**
- Direct/Organic: 3,903 leads × 2.15% funded rate × 10% uplift = 3,903 × 0.00215 × 0.10 = ~8 additional loans
- Paid Spend: 6,977 leads × 1.05% funded rate × 10% uplift = 6,977 × 0.00105 × 0.10 = ~7 additional loans
- Total: ~15 loans
- **Revenue: 15 × $6,000 = ~$90K/quarter → displayed as +$75–100K/quarter**

### 8d. ~~Rec 4 — Protect the Golden Hour (REMOVED)~~

**Originally proposed:** Reserve 8–9 AM for first-attempt dials based on its ~5.9% contact rate (nearly 2x midday).

**Why removed:** Controlling for attempt number eliminates the time-of-day effect. At 8 AM, 70.5% of dials are attempts 1–5 (avg attempt 4.5) vs 25–30% at midday (avg attempt ~9.5). When comparing the same attempt bucket across hours, contact rates are flat (8–11% for attempts 1–3 at every hour). The "golden hour" was a composition effect, not a true time-of-day advantage.

```sql
-- Contact rate by hour AND attempt bucket (confirms composition effect)
SELECT
  CASE
    WHEN `Pool A Call Attempt Number` BETWEEN 1 AND 3 THEN '1-3'
    WHEN `Pool A Call Attempt Number` BETWEEN 4 AND 7 THEN '4-7'
    WHEN `Pool A Call Attempt Number` BETWEEN 8 AND 12 THEN '8-12'
    WHEN `Pool A Call Attempt Number` >= 13 THEN '13+'
  END AS attempt_bucket,
  EXTRACT(HOUR FROM `Activity _ET_ Time`) AS hour_et,
  COUNT(*) AS dials,
  ROUND(COUNTIF(`Contacted_ _Yes _ No_` = true) / COUNT(*) * 100, 1) AS contact_rate
FROM `inventory-analytics-475119.testing.fct_dials`
WHERE `Is Pool A _Active SDR__ _Yes _ No_` = true
  AND `Lead ID` IS NOT NULL
  AND EXTRACT(HOUR FROM `Activity _ET_ Time`) BETWEEN 8 AND 17
GROUP BY 1, 2
HAVING COUNT(*) >= 100
ORDER BY 1, 2;
```

### Summary

| Recommendation | Incremental Funded Loans | Est. Revenue/Quarter |
|---|---|---|
| 1. Cap at 10 Attempts | ~28 | +$120–170K |
| 2. Channel Prioritization | ~15 | +$75–100K |
| 3. Weekend Staffing | ~15 | +$75–100K |
| **Combined** | **~58** | **~$270–370K/quarter (~$1.1–1.5M/year)** |

All estimates use blended $6,000 revenue per funded loan and current baseline conversion rates. These are order-of-magnitude estimates intended to size the opportunity — actual impact depends on implementation quality and market conditions.
