# Medical Telegram Data Warehouse

## Project Overview
This project builds a **data warehouse** for Telegram messages related to medical topics. It leverages **dbt** to transform raw message data into a **star schema** with staging and mart layers, enabling analytics on channels, messages, and user engagement.

## Project Objectives
- Extract, transform, and load Telegram message data.
- Create **dimensional models**: `dim_channels`, `dim_dates`, `fct_messages`.
- Implement **data quality tests** to ensure accuracy.
- Generate **dbt documentation** for reporting and review.

## Star Schema
- **Fact Table:** `fct_messages` – records each message with metrics like views, forwards, and content length.
- **Dimension Tables:**  
  - `dim_channels` – unique Telegram channels with metadata.  
  - `dim_dates` – calendar dimension for message timestamps.  
- Enables efficient querying for analytics, trends, and KPIs.

## dbt Structure
- `models/staging/` – staging models for raw tables.  
- `models/marts/` – transformed fact and dimension tables.  
- `models/schema.yml` – descriptions and tests for all models.  
- `tests/` – custom dbt tests for data quality (e.g., no future messages, positive views).

## Testing & Validation
All dbt tests pass, ensuring:
- Non-null and unique keys.
- Referential integrity between facts and dimensions.
- Business logic validations.

## CI/CD
- GitHub Actions runs dbt workflow for Task 2:
  - Install dependencies
  - Run models
  - Run tests
  - Generate documentation

## Documentation
- Generated via:
  ```bash
  dbt docs generate
  dbt docs serve

Repo Structure
medical-telegram-warehouse/
├─ medical_warehouse/ # Main dbt project
│ ├─ dbt_project.yml # dbt project configuration
│ ├─ profiles.yml # Connection profiles
│ ├─ .user.yml # Optional user-specific settings
│ ├─ models/ # All dbt models
│ │ ├─ staging/ # Staging layer models (raw table transformations)
│ │ │ ├─ stg_telegram_messages.sql # Staging model for Telegram messages
│ │ │ └─ schema.yml # Descriptions and tests for staging models
│ │ ├─ marts/ # Data marts / dimensional models
│ │ │ ├─ dim_channels.sql # Dimension table for channels
│ │ │ ├─ dim_dates.sql # Dimension table for dates
│ │ │ ├─ fct_messages.sql # Fact table for messages
│ │ │ └─ schema.yml # Descriptions and tests for marts
│ ├─ tests/ # Custom dbt tests
│ │ ├─ assert_no_future_messages.sql # Test to ensure no future-dated messages
│ │ └─ assert_positive_views.sql # Test to ensure message views are positive
│ └─ macros/ # Custom macros if any (empty or reused from dbt)
│
├─ src/ # Python scripts for raw data loading
│ └─ load_raw_data.py # Script to load raw Telegram messages
│
├─ requirements.txt # Python dependencies
│
├─ .github/workflows/ # GitHub Actions CI/CD workflows
│ └─ unittests.yml # Workflow for running dbt models, tests, docs
│
├─ target/ # dbt build output (auto-generated)
│ ├─ catalog.json
│ ├─ graph.gpickle
│ ├─ index.html # Generated documentation
│ ├─ manifest.json
│ ├─ run_results.json
│ ├─ compiled/ # Compiled SQL from dbt models
│ └─ run/ # Run-time artifacts
│
└─ README.md # Project overview and instructions