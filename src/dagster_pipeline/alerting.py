from dagster import failure_hook


@failure_hook
def notify_failure(context):
    context.log.error(f"❌ Pipeline failed in: {context.job_name}")