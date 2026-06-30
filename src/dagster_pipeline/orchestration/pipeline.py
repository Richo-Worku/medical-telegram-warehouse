from dagster import op, job


@op
def scrape_telegram_data():
    pass


@op
def load_raw_to_postgres():
    pass


@op
def run_dbt_transformations():
    pass


@op
def run_yolo_enrichment():
    pass


@job
def telegram_analytics_pipeline():
    run_yolo_enrichment(
        run_dbt_transformations(
            load_raw_to_postgres(
                scrape_telegram_data()
            )
        )
    )