from dagster import op, job
import subprocess


# -------------------------
# OP 1: SCRAPE
# -------------------------
@op
def scrape_telegram_data():
    subprocess.run(
        ["python", "src/scraping/telegram_scraper.py"],
        check=True
    )
    return "scrape_done"


# -------------------------
# OP 2: LOAD TO POSTGRES
# -------------------------
@op
def load_raw_to_postgres():
    subprocess.run(
        ["python", "src/load/load_to_postgres.py"],
        check=True
    )
    return "load_done"


# -------------------------
# OP 3: DBT TRANSFORMATIONS
# -------------------------
@op
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run"],
        cwd="dbt",
        check=True
    )
    return "dbt_done"


# -------------------------
# OP 4: YOLO ENRICHMENT
# -------------------------
@op
def run_yolo_enrichment():
    subprocess.run(
        ["python", "src/yolo/yolo_enrichment.py"],
        check=True
    )
    return "yolo_done"


# -------------------------
# JOB (PIPELINE GRAPH)
# -------------------------
@job
def telegram_analytics_pipeline():

    # Step 1 → Scrape
    scrape_telegram_data()

    # Step 2 → Load
    load_raw_to_postgres()

    # Step 3 → dbt
    run_dbt_transformations()

    # Step 4 → YOLO
    run_yolo_enrichment()