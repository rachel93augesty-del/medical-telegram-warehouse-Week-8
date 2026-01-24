# dagster_pipeline/pipeline.py
from dagster import op, job
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scraper/run_scraper.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "etl/load_raw.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run"], cwd="dbt", check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "yolo/run_detection.py"], check=True)

@job
def telegram_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
