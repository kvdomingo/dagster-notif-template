from dagster import Definitions, load_assets_from_package_module, EnvVar

from src.email import AwsSesResource
from src.sensors import (
    email_notify_on_run_failure_sensor,
    slack_notify_on_run_failure_sensor,
)
from src.assets import debug
from src.settings import settings

defs = Definitions(
    assets=[
        *load_assets_from_package_module(debug, "debug", "debug"),
    ],
    resources={
        "ses": AwsSesResource(
            region=settings.AWS_REGION,
            access_key=EnvVar("AWS_SES_ACCESS_KEY"),
            secret_key=EnvVar("AWS_SES_SECRET_KEY"),
            sender_email=EnvVar("SENDER_EMAIL"),
            configuration_set=EnvVar("AWS_SES_CONFIGURATION_SET"),
            email_recipients=settings.ALERT_EMAIL_RECIPIENTS,
        ),
    },
    sensors=[
        email_notify_on_run_failure_sensor,
        slack_notify_on_run_failure_sensor,
    ],
)
