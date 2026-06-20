# Power BI Dashboard Specification

## Purpose

The Power BI dashboard turns the LeadOS BI export dataset into a portfolio-ready view of lead opportunity, digital-presence gaps, outreach priority, and import quality.

This specification prepares the manual dashboard build. It does not add a Power BI binary, automation, frontend, API route, external storage, or new dependency.

## Intended Audience

- LeadOS operators reviewing local-business lead quality.
- Sales or outreach reviewers prioritizing human follow-up.
- Portfolio reviewers evaluating the reporting and dashboard design of the MVP.

## Dataset Source

Use the LeadOS BI export dataset documented in `docs/BI_EXPORT.md`.

Dataset name:

```text
leados_reporting_dataset
```

The source concept is the backend `BIExportService`, which converts SQL-backed `ReportRepository` outputs into stable, flat CSV-ready tables. The sample fixtures in `data/bi_exports/*.csv` are deterministic demo inputs for manually building the first Power BI report.

## Table List

| BI export table | Source report | Primary dashboard use |
|---|---|---|
| `leads_by_city_category` | `leads_by_city_and_category` | Lead volume by location and market category |
| `missing_website_leads` | `leads_missing_website` | Leads with an obvious website gap |
| `high_review_weak_presence_leads` | `high_review_weak_presence_leads` | Strong offline demand with weak visible digital presence |
| `manual_review_leads` | `manual_review_leads` | Human-review outreach queue |
| `score_distribution_by_category` | `score_distribution_by_category` | Opportunity score mix by category |
| `import_quality_summary` | `import_quality_summary` | CSV import quality and failure rates |
| `missing_data_report` | `missing_data_report` | Lead-level missing data and scoring completeness gaps |

## Expected CSV Inputs

Load these CSV files from `data/bi_exports/`:

| CSV file | Required headers |
|---|---|
| `leads_by_city_category.csv` | `city`, `category`, `lead_count` |
| `missing_website_leads.csv` | `lead_id`, `business_name`, `city`, `category`, `website` |
| `high_review_weak_presence_leads.csv` | `lead_id`, `business_name`, `city`, `category`, `review_count`, `priority_label`, `confidence_level`, `weak_signals` |
| `manual_review_leads.csv` | `lead_id`, `business_name`, `city`, `category`, `total_score`, `priority_label`, `confidence_level`, `missing_data`, `risk_flags` |
| `score_distribution_by_category.csv` | `category`, `priority_label`, `lead_count`, `average_score` |
| `import_quality_summary.csv` | `import_run_id`, `source_name`, `total_records`, `valid_records`, `invalid_records`, `duplicate_records`, `error_count`, `created_at` |
| `missing_data_report.csv` | `lead_id`, `business_name`, `city`, `category`, `missing_fields`, `score_missing_data` |

## Relationships And Modeling Guidance

- Treat each CSV as a flat fact-style table for the first dashboard build.
- Use `category` as a shared slicer across `leads_by_city_category`, `score_distribution_by_category`, `manual_review_leads`, `missing_website_leads`, `high_review_weak_presence_leads`, and `missing_data_report`.
- Use `city` as a shared slicer across lead-level and volume tables.
- Do not force relationships on `lead_id` unless a future export adds a canonical lead dimension. Several current tables are already aggregated.
- Keep `import_quality_summary` separate from lead-level tables because it describes import runs, not individual leads.
- Format `created_at` as a datetime column.
- Keep `total_score` and `average_score` as decimal numbers.
- Keep `lead_count`, `review_count`, and import count columns as whole numbers.

## Core Dashboard Pages

### Executive Overview

Purpose: summarize lead volume, priority mix, digital gaps, and import quality.

Visuals:

- Card: total leads from `leads_by_city_category[lead_count]`.
- Clustered bar chart: leads by city/category from `leads_by_city_category`.
- Stacked bar chart: score distribution by category from `score_distribution_by_category`.
- Card: missing website lead count from `missing_website_leads`.
- Card: manual-review queue count from `manual_review_leads`.
- Table: import quality summary from `import_quality_summary`.

### Lead Opportunity Map

Purpose: show where lead opportunity is concentrated by city and category.

Visuals:

- Bar chart: leads by city/category from `leads_by_city_category`.
- Matrix: city by category with lead count.
- Donut or stacked bar: category share by lead count.
- Table: high-review weak-presence leads from `high_review_weak_presence_leads`.

### Digital Gap Analysis

Purpose: highlight businesses with visible digital-presence gaps.

Visuals:

- Table: missing website leads from `missing_website_leads`.
- Table: high-review weak-presence leads from `high_review_weak_presence_leads`.
- Bar chart: weak-presence count by category.
- Bar chart: missing-data breakdown from `missing_data_report`.

### Outreach Priority Queue

Purpose: give a human reviewer a clean queue of outreach candidates.

Visuals:

- Table: manual-review queue from `manual_review_leads`.
- Bar chart: priority label distribution from `manual_review_leads`.
- Bar chart: score distribution by category from `score_distribution_by_category`.
- Card: average score from `manual_review_leads[total_score]`.

### Import Quality & Data Completeness

Purpose: show whether source data is clean enough to trust downstream scoring and outreach decisions.

Visuals:

- Table: import quality summary from `import_quality_summary`.
- Cards: total records, valid records, invalid records, duplicate records, and error count.
- Table: missing-data breakdown from `missing_data_report`.
- Bar chart: missing field count by category from `missing_data_report`.

## Recommended Slicers

- City
- Category
- Priority label
- Confidence level
- Source name
- Created date

## Key Measures

Recommended Power BI measures:

```text
Total Leads = SUM(leads_by_city_category[lead_count])
Missing Website Leads = COUNTROWS(missing_website_leads)
High Review Weak Presence Leads = COUNTROWS(high_review_weak_presence_leads)
Manual Review Queue = COUNTROWS(manual_review_leads)
Average Manual Review Score = AVERAGE(manual_review_leads[total_score])
Valid Import Rate = DIVIDE(SUM(import_quality_summary[valid_records]), SUM(import_quality_summary[total_records]))
Invalid Import Rate = DIVIDE(SUM(import_quality_summary[invalid_records]), SUM(import_quality_summary[total_records]))
Duplicate Import Rate = DIVIDE(SUM(import_quality_summary[duplicate_records]), SUM(import_quality_summary[total_records]))
```

## Manual Power BI Build Steps

1. Open Power BI Desktop manually.
2. Import all CSV files from `data/bi_exports/`.
3. Confirm table names match the CSV stems and BI export table names.
4. Set data types according to the expected CSV input section.
5. Add slicers for city, category, priority label, confidence level, source name, and created date.
6. Create the recommended measures.
7. Build the five dashboard pages listed above.
8. Save the `.pbix` file manually outside this repository unless a future task explicitly allows adding it.

`.pbix` creation is intentionally manual and deferred. This repository should not contain a `.pbix` file for TASK-0701.

## Portfolio Screenshot Checklist

- Executive Overview shows total leads, missing website leads, manual-review queue, and import quality.
- Lead Opportunity Map shows a clear city/category breakdown.
- Digital Gap Analysis shows missing website and high-review weak-presence tables.
- Outreach Priority Queue shows priority labels, confidence levels, scores, and review blockers.
- Import Quality & Data Completeness shows import run quality and missing-data breakdown.
- Screenshots use sample data only and do not expose private lead data.

## Intentionally Not Included Yet

- `.pbix` file
- Power BI Desktop automation
- Frontend or embedded dashboard
- API route or file download endpoint
- External storage
- pandas or new dependencies
- AI analytics
- CRM integration
- ProjectOS integration
- Content Creation Automation integration
- Automatic outbound sending
