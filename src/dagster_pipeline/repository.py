from dagster import Definitions
from .jobs import telegram_analytics_pipeline


defs = Definitions(
    jobs=[telegram_analytics_pipeline]
)