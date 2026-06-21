# stedi-human-balance-analytics
AWS data lakehouse project using S3, Glue, Spark, and Athena to curate STEDI Step Trainer sensor data for machine learning.

# STEDI Human Balance Analytics

This project builds an AWS data lakehouse pipeline for STEDI Step Trainer sensor data.

## Tools Used
- AWS S3
- AWS Glue
- AWS Athena
- Python
- PySpark
- GitHub

## Pipeline
The project processes customer, accelerometer, and Step Trainer JSON data through landing, trusted, and curated zones.

## Final Row Counts
| Table | Rows |
|---|---:|
| customer_landing | 956 |
| accelerometer_landing | 81,273 |
| step_trainer_landing | 28,680 |
| customer_trusted | 482 |
| accelerometer_trusted | 40,981 |
| customers_curated | 482 |
| step_trainer_trusted | 14,460 |
| machine_learning_curated | 43,681 |

## Repository Contents
- `glue_jobs/` — AWS Glue PySpark jobs
- `sql/` — Athena landing-table scripts
- `screenshots/` — Athena query-result screenshots
