# Data Model

## Tables

### leads

Stores normalized business leads.

Important columns:

```text
id
business_name
normalized_business_name
category
normalized_category
city
normalized_city
state
phone
website
rating
review_count
address
source_url
created_at
updated_at
```

Uniqueness rule:

```text
normalized_business_name + normalized_city
```

### lead_import_runs

Stores each import execution summary.

```text
id
source_name
total_records
valid_records
invalid_records
duplicate_records
created_at
```

### lead_import_errors

Stores rejected CSV rows and validation reasons.

```text
id
import_run_id
row_number
reasons
raw_row
created_at
```

### lead_audits

Reserved for deterministic website audit persistence.

```text
id
lead_id
requested_url
fetch_status
result_json
created_at
```

### lead_scores

Reserved for score persistence.

```text
id
lead_id
scoring_version
total_score
category_scores
priority_label
confidence_level
reason_summary
positive_signals
risk_flags
missing_data
created_at
```

## Current database strategy

SQLite is the default for local development. PostgreSQL should be the production target after migrations are introduced.
