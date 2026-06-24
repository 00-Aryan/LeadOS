# Tableau Dashboard Specification

## Purpose

The Tableau dashboard turns the LeadOS BI export dataset into a portfolio-ready workbook plan for lead opportunity, digital-presence gaps, outreach priority, and import quality.

This specification prepares a manual Tableau workbook build. It does not add a Tableau workbook binary, Tableau automation, frontend, API route, external storage, scheduler, or new dependency.

## Audience

- LeadOS operators reviewing local-business lead quality.
- Sales or outreach reviewers prioritizing human follow-up.
- Portfolio reviewers evaluating the reporting and dashboard design of the MVP.

## Input CSV Fixtures

Use the LeadOS BI export dataset documented in `docs/BI_EXPORT.md`.

Dataset name:

```text
leados_reporting_dataset
```

Load these CSV files from `data/bi_exports/`:

| CSV file | BI export table | Dashboard use |
|---|---|---|
| `leads_by_city_category.csv` | `leads_by_city_category` | Lead volume by city and category |
| `missing_website_leads.csv` | `missing_website_leads` | Leads with visible website gaps |
| `high_review_weak_presence_leads.csv` | `high_review_weak_presence_leads` | Strong offline demand with weak visible digital presence |
| `manual_review_leads.csv` | `manual_review_leads` | Human-review outreach queue |
| `score_distribution_by_category.csv` | `score_distribution_by_category` | Priority and score mix by category |
| `import_quality_summary.csv` | `import_quality_summary` | CSV import quality and failure rates |
| `missing_data_report.csv` | `missing_data_report` | Lead-level missing data and scoring completeness gaps |

Expected headers:

| CSV file | Required headers |
|---|---|
| `leads_by_city_category.csv` | `city`, `category`, `lead_count` |
| `missing_website_leads.csv` | `lead_id`, `business_name`, `city`, `category`, `website` |
| `high_review_weak_presence_leads.csv` | `lead_id`, `business_name`, `city`, `category`, `review_count`, `priority_label`, `confidence_level`, `weak_signals` |
| `manual_review_leads.csv` | `lead_id`, `business_name`, `city`, `category`, `total_score`, `priority_label`, `confidence_level`, `missing_data`, `risk_flags` |
| `score_distribution_by_category.csv` | `category`, `priority_label`, `lead_count`, `average_score` |
| `import_quality_summary.csv` | `import_run_id`, `source_name`, `total_records`, `valid_records`, `invalid_records`, `duplicate_records`, `error_count`, `created_at` |
| `missing_data_report.csv` | `lead_id`, `business_name`, `city`, `category`, `missing_fields`, `score_missing_data` |

## Data Source Setup

1. Open Tableau Desktop manually.
2. Connect to each CSV file in `data/bi_exports/`.
3. Keep each table name aligned with the CSV stem and BI export table name.
4. Treat the first row as headers.
5. Assign data types manually:

| Column type | Tableau type guidance |
|---|---|
| `lead_id`, `import_run_id` | Number whole |
| `lead_count`, `review_count`, import count columns | Number whole |
| `total_score`, `average_score` | Number decimal |
| `created_at` | Date & Time |
| `business_name`, `city`, `category`, `priority_label`, `confidence_level`, `source_name` | String |
| `missing_data`, `risk_flags`, `weak_signals`, `missing_fields`, `score_missing_data` | String / text detail |

6. Do not force physical relationships between all CSVs for the first workbook.
7. Use `city`, `category`, `priority_label`, and `confidence_level` as dashboard filters instead of assuming a canonical lead dimension exists.
8. Keep `import_quality_summary` separate from lead-level tables because it describes import runs, not individual leads.

## Dashboard Pages

The Tableau workbook should contain five dashboards.

### Executive Lead Overview

Purpose: summarize total opportunity, visible digital gaps, manual-review load, and import quality.

Recommended content:

- KPI: total leads from `leads_by_city_category`.
- KPI: missing website leads from `missing_website_leads`.
- KPI: manual-review queue count from `manual_review_leads`.
- Bar chart: leads by city and category from `leads_by_city_category`.
- Stacked bar chart: score distribution by category from `score_distribution_by_category`.
- Table: latest import quality summary from `import_quality_summary`.

### Market/Category Opportunity

Purpose: show where opportunity is concentrated by geography and category.

Recommended content:

- Heatmap: `city` by `category` with `lead_count`.
- Bar chart: top categories by lead count.
- Bar chart: top cities by lead count.
- Table: high-review weak-presence leads from `high_review_weak_presence_leads`.
- Tooltip detail: business name, city, category, review count, priority label, and weak signals.

### Digital Gap Prioritization

Purpose: identify businesses where digital-presence gaps create a practical outreach angle.

Recommended content:

- Table: missing website leads from `missing_website_leads`.
- Table: high-review weak-presence leads from `high_review_weak_presence_leads`.
- Bar chart: weak-presence leads by category.
- Bar chart: missing-data count by category from `missing_data_report`.
- Detail table: `missing_fields` and `score_missing_data` from `missing_data_report`.

### Outreach Queue

Purpose: give a human reviewer a clear queue without enabling automatic outbound sending.

Recommended content:

- Table: manual-review leads from `manual_review_leads`.
- Bar chart: priority label distribution from `manual_review_leads`.
- Bar chart: confidence-level distribution from `manual_review_leads`.
- Scatter plot: `total_score` by category or city from `manual_review_leads`.
- Detail columns: missing data and risk flags.

### Data Quality Monitor

Purpose: show whether imported data is clean enough to trust scoring and outreach decisions.

Recommended content:

- KPI: total imported records from `import_quality_summary`.
- KPI: valid records from `import_quality_summary`.
- KPI: invalid records from `import_quality_summary`.
- KPI: duplicate records from `import_quality_summary`.
- KPI: error count from `import_quality_summary`.
- Table: import quality by source name and created timestamp.
- Table: missing-data report from `missing_data_report`.

## Worksheets

Create these worksheets before assembling dashboards:

| Worksheet | Source table | Recommended mark type |
|---|---|---|
| Total Leads KPI | `leads_by_city_category` | Text |
| Missing Website KPI | `missing_website_leads` | Text |
| Manual Review KPI | `manual_review_leads` | Text |
| Leads By City Category | `leads_by_city_category` | Bar |
| City Category Heatmap | `leads_by_city_category` | Square / highlight table |
| Score Distribution | `score_distribution_by_category` | Stacked bar |
| Missing Website Leads Table | `missing_website_leads` | Text table |
| High Review Weak Presence Table | `high_review_weak_presence_leads` | Text table |
| Manual Review Queue Table | `manual_review_leads` | Text table |
| Priority Distribution | `manual_review_leads` | Bar |
| Confidence Distribution | `manual_review_leads` | Bar |
| Manual Score Scatter | `manual_review_leads` | Circle |
| Import Quality Summary | `import_quality_summary` | Text table |
| Import Quality KPIs | `import_quality_summary` | Text |
| Missing Data Table | `missing_data_report` | Text table |
| Missing Data By Category | `missing_data_report` | Bar |

## Filters

Recommended dashboard filters:

- City
- Category
- Priority label
- Confidence level
- Source name
- Created date

Filter guidance:

- Apply `city` and `category` filters to lead-level and lead-volume dashboards.
- Apply `priority_label` and `confidence_level` filters to outreach and score dashboards.
- Apply `source_name` and `created_at` filters only to import quality views.
- Avoid cross-filter actions that imply row-level relationships between aggregated tables and lead-level tables unless a future canonical lead dimension is exported.

## Calculated Fields

Recommended Tableau calculated fields:

```text
Valid Import Rate = SUM([valid_records]) / SUM([total_records])
Invalid Import Rate = SUM([invalid_records]) / SUM([total_records])
Duplicate Import Rate = SUM([duplicate_records]) / SUM([total_records])
Manual Review Queue Size = COUNT([lead_id])
Missing Website Lead Count = COUNT([lead_id])
Average Manual Review Score = AVG([total_score])
```

Formatting guidance:

- Format import rates as percentages.
- Format score fields with one decimal place.
- Format record counts as whole numbers.
- Use null-safe handling when a worksheet has no rows.

## Tooltip Guidance

Tooltips should explain why a lead appears in a view. Recommended tooltip fields:

| Dashboard | Tooltip fields |
|---|---|
| Executive Lead Overview | city, category, lead count, priority label |
| Market/Category Opportunity | city, category, lead count, review count |
| Digital Gap Prioritization | business name, website, weak signals, missing fields |
| Outreach Queue | business name, total score, priority label, confidence level, risk flags, missing data |
| Data Quality Monitor | source name, total records, valid records, invalid records, duplicate records, error count |

Keep tooltip language factual. Do not imply that outreach has been sent. Do not infer causes beyond fields present in the CSV exports.

## Manual Tableau Build Steps

1. Open Tableau Desktop manually.
2. Connect to all CSV fixtures in `data/bi_exports/`.
3. Confirm table names match the BI export table names.
4. Set data types according to the data source setup section.
5. Build the worksheets listed above.
6. Add the five dashboards:
   - Executive Lead Overview
   - Market/Category Opportunity
   - Digital Gap Prioritization
   - Outreach Queue
   - Data Quality Monitor
7. Add dashboard filters for city, category, priority label, confidence level, source name, and created date.
8. Add calculated fields for import rates, queue size, missing website count, and average manual review score.
9. Save the Tableau workbook manually outside this repository unless a future task explicitly allows committing Tableau workbook files.

Tableau workbook creation is manual and deferred. This repository should not contain `.twb`, `.twbx`, or `.hyper` files for TASK-0702.

## Portfolio Screenshot Checklist

- Executive Lead Overview shows total leads, missing website leads, manual-review queue, and import quality.
- Market/Category Opportunity shows city/category opportunity concentration.
- Digital Gap Prioritization shows missing website and high-review weak-presence leads.
- Outreach Queue shows priority labels, confidence levels, total scores, missing data, and risk flags.
- Data Quality Monitor shows import run quality and missing-data coverage.
- Screenshots use sample data only and do not expose private lead data.
- Screenshot captions should state that Tableau workbook creation is manual and based on deterministic sample BI export fixtures.

## Deferred Work

Intentionally not included:

- `.twb` file
- `.twbx` file
- `.hyper` extract
- Tableau Desktop automation
- Tableau Server or Tableau Cloud publishing
- Frontend or embedded dashboard
- API route or file download endpoint
- Scheduled export jobs
- External storage
- pandas or new dependencies
- AI analytics
- CRM integration
- ProjectOS integration
- Content Creation Automation integration
- Automatic outbound sending
