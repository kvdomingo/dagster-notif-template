from dagster import (
    DefaultSensorStatus,
    RunFailureSensorContext,
    run_failure_sensor,
)
from dagster_slack import make_slack_on_run_failure_sensor

from src.email import AwsSesResource
from src.settings import settings


slack_notify_on_run_failure_sensor = make_slack_on_run_failure_sensor(
    name="slack_notify_on_run_failure_sensor",
    channel=f"#{settings.SLACK_CHANNEL}",
    slack_token=settings.SLACK_TOKEN,
    webserver_base_url=settings.DAGSTER_BASE_URL,
    monitor_all_code_locations=True,
    default_status=DefaultSensorStatus.RUNNING,
    minimum_interval_seconds=settings.DEFAULT_SENSOR_INTERVAL_SECONDS,
)


@run_failure_sensor(
    default_status=DefaultSensorStatus.RUNNING,
    minimum_interval_seconds=settings.DEFAULT_SENSOR_INTERVAL_SECONDS,
    monitor_all_code_locations=True,
)
def email_notify_on_run_failure_sensor(
    context: RunFailureSensorContext, ses: AwsSesResource
):
    """
    This function defines any API call(s) needed to send an email using the email service of your choice. For this
    template, AWS SES is used. Consult the docs for your email service to determine the correct API call(s) to use.
    """
    ses.send_email(
        context,
        subject=f"{settings.APPLICATION_NAME} Dagster Run Failure",
        html=f"""
        <html>
            <body>
                <p>
                    Job <b>{context.dagster_run.job_name}</b> ({context.dagster_run.run_id}) failed.</b>
                </p>
                <p>
                    <a href="{settings.DAGSTER_BASE_URL}/runs/{context.dagster_run.run_id}">
                        View in Dagster UI
                    </a>
                </p>
                <p>
                    {settings.APPLICATION_NAME} Dagster Mailer
                </p>
            </body>
        </html>
        """.strip(),
        text=f"""
        Job "{context.dagster_run.job_name}" ({context.dagster_run.run_id}) failed.

        View in Dagster UI: {settings.DAGSTER_BASE_URL}/runs/{context.dagster_run.run_id}

        {settings.APPLICATION_NAME} Dagster Mailer
        """.strip(),
    )
