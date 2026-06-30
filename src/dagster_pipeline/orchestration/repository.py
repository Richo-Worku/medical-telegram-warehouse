from dagster import Definitions

from .jobs import telegram_analytics_pipeline
from .schedule import daily_pipeline_schedule

defs = Definitions(
    jobs=[telegram_analytics_pipeline],
    schedules=[daily_pipeline_schedule],
)