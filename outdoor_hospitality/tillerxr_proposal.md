# BUSINESS PROPOSAL

## Outdoor Hospitality Benchmarking MVP

**Prepared for:** Lizzy Bustamante, TillerXR
**Date:** March 6, 2026

---

## PROBLEM

1. **No benchmarking standard for outdoor hospitality**
The hotel industry has had the STAR report since the 1980s. The ~27,000 U.S. campgrounds have nothing comparable. Multi-park operators and institutional investors entering the space have zero visibility into how their parks perform relative to peers on Occupancy, ADR, or RevPAS.

2. **Performance data is siloed across PMS platforms**
Operators with parks spread across New Book, Camp Spot, and other reservation systems can't see a unified picture. Camp Spot's "Signals" only benchmarks Camp Spot customers. There is no PMS-agnostic data layer for the industry.

3. **Manual reporting doesn't scale**
Revenue managers pull reports from their PMS, clean them in Excel or Power BI, and try to assess portfolio performance manually. This is time-consuming, error-prone, and impossible to scale across 40+ parks.

---

## SOLUTION

Build a data pipeline that ingests performance data from the New Book API for 50 founding parks, calculates the three core KPIs (Occupancy, ADR, RevPAS), and surfaces them in internal Looker Studio dashboards for validation and stakeholder review.

**What You'll Get:**

- **Automated Data Pipeline** -- Daily ingestion from New Book API into BigQuery, orchestrated by Dagster
- **Standardized Data Model** -- dbt Core models defining benchmarking schema, KPI calculations, and comp set logic
- **Core KPI Calculations** -- Occupancy Rate, Average Daily Rate, and Revenue Per Available Site across all participating parks with 12 months of historical data
- **Internal Validation Dashboards** -- Looker Studio dashboards to review KPIs by park, region, and unit type (RV, cabins, tents) against comp set averages
- **Documentation & Training** -- Technical docs, data dictionary, and a live walkthrough session

---

## SCOPE OF WORK

### MVP Deliverables

- Custom Python ingestion from New Book API (reservations, inventory, revenue data)
- Dagster orchestration with scheduled daily refreshes
- BigQuery data warehouse setup and configuration
- dbt Core data models for standardized schema and KPI logic
- Looker Studio dashboard suite (KPI overview, comp set comparison, unit type breakdown)
- 12-month historical backfill for all 50 founding parks
- Documentation and live training session
- 2 weeks post-launch support

### What's NOT Included (Future Phases)

- Client-facing UI or polished product dashboard
- Additional PMS integrations (Camp Spot, Firefly, etc.)
- Interactive comp set builder
- Automated alerts or notifications

---

## DELIVERABLES AND TIMELINE

**Total Timeline: ~6 Weeks**

| Phase | Timeframe | Deliverables |
|-------|-----------|-------------|
| **1. Data Infrastructure** | Weeks 1-2 | New Book API ingestion, Dagster pipelines, BigQuery schema, historical backfill |
| **2. Data Modeling & KPIs** | Weeks 3-4 | dbt models, Occupancy/ADR/RevPAS calculations, comp set logic, data validation |
| **3. Dashboards & Handoff** | Weeks 5-6 | Looker Studio dashboards, end-to-end testing, documentation, training session |

**Post-Launch:** 2 weeks of support for questions and adjustments.

---

## PRICING

**Fixed Project Price: $3,500**

This covers all deliverables above, up to 6 weeks of development, testing, training, documentation, and two weeks of post-launch support.

**Payment Terms (via Google Docs contract):**

- **Milestone 1 — $1,750** upon completion of:
  - New Book API ingestion pipeline built and tested
  - Dagster orchestration running on schedule
  - BigQuery warehouse set up with data flowing
- **Milestone 2 — $1,750** upon delivery of:
  - All dbt models and KPI calculations validated
  - Looker Studio dashboard suite complete
  - Documentation delivered and training completed

**Ongoing Infrastructure Costs (Client-Paid): ~$150/month**
- Google Cloud / BigQuery
- Dagster Cloud
- Looker Studio: FREE

---

## SUCCESS CRITERIA

The project is complete when:

- New Book API data syncs daily into BigQuery for all 50 founding parks
- 12 months of historical data is backfilled and validated
- Occupancy, ADR, and RevPAS calculations are accurate and reconciled against operator reports
- Looker Studio dashboards display KPIs by park, region, and unit type
- Comp set averages and indexing are functional
- Documentation is delivered and team is trained
- You confirm the system is working and ready for stakeholder review

---

## NEXT STEPS

1. Review this proposal and confirm the scope
2. Coordinate New Book API access (sandbox + production credentials)
3. Sign contract and fund Milestone 1 to begin work
4. I begin immediately and provide weekly progress updates

**Timeline:** I can start as soon as API access is provided and deliver the complete MVP within 6 weeks.

---

Truett Bloxsom
truett@marginmindai.com
