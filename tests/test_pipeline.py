import pytest
from dagster import execute_job, DagsterInstance
from dagster_pipeline.pipeline import telegram_data_pipeline

# Patch external ops
@pytest.fixture(autouse=True)
def mock_external_ops(mocker):
    mocker.patch("dagster_pipeline.pipeline.scrape_telegram_data", return_value=None)
    mocker.patch("dagster_pipeline.pipeline.load_raw_to_postgres", return_value=None)
    mocker.patch("dagster_pipeline.pipeline.run_dbt_transformations", return_value=None)
    mocker.patch("dagster_pipeline.pipeline.run_yolo_enrichment", return_value=None)

def test_pipeline_runs():
    # Create a temporary Dagster instance for testing
    instance = DagsterInstance.ephemeral()
    result = execute_job(telegram_data_pipeline, instance=instance)
    assert result.success
