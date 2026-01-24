from dagster import schedule
from dagster_pipeline.pipeline import telegram_data_pipeline

# Daily at 2 AM Addis Ababa time
@schedule(
    cron_schedule="0 2 * * *",
    job=telegram_data_pipeline,
    execution_timezone="Africa/Addis_Ababa"
)
def daily_telegram_pipeline():
    return {}  # no config needed for now
