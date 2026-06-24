# BI Export Dataset Layer

## Purpose

The BI export layer converts SQL-backed LeadOS reporting outputs into stable, flat datasets for later dashboard work. It prepares the backend shape needed by Power BI, Tableau, or similar tools without adding a dashboard, file endpoint, scheduler, external storage, or new dependency.

The layer consumes the read-only `ReportRepository` outputs and formats them into named tables with explicit columns, rows, row counts, source report names, and generated timestamps.

## Dataset

The standard dataset is:

```text
leados_reporting_dataset
```

It contains these dashboard-ready tables:

- `leads_by_city_category`
- `missing_website_leads`
- `high_review_weak_presence_leads`
- `manual_review_leads`
- `score_distribution_by_category`
- `import_quality_summary`
- `missing_data_report`

## Dashboard Readiness

Each table has stable column ordering and flat row values. Empty reports still include explicit headers so dashboard authors can wire visuals before live data exists.

CSV conversion uses Python standard library only and returns strings. The service does not write files to disk. `None` values become empty cells, and list or dictionary values become deterministic JSON strings.

## Not Included Yet

This layer intentionally does not include:

- Power BI dashboards
- Tableau dashboards
- frontend views
- API routes
- file download endpoints
- scheduled jobs
- external storage
- pandas or other new dependencies
- AI analytics
- CRM, ProjectOS, or Content Creation Automation integrations

## Future Dashboard Work

A later Power BI or Tableau task should consume this dataset conceptually and map visuals to these stable table names and columns. Dashboard work must wait until TASK-0208 is committed, pushed, and Backend CI is green.
