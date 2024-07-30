from boto3 import client as boto3_client

from dagster import ConfigurableResource, RunFailureSensorContext


class AwsSesResource(ConfigurableResource):
    """
    This class defines a Dagster resource object which initializes the email client with the necessary parameters, and
    defines the logic for sending emails. Adjust this depending on the email service you are using, or define a new
    resource if you need to use multiple notification methods.
    """

    region: str
    access_key: str
    secret_key: str
    configuration_set: str
    sender_email: str
    email_recipients: list[str]

    def get_client(self):
        return boto3_client(
            "ses",
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def send_email(
        self,
        context: RunFailureSensorContext,
        subject: str,
        html: str,
        text: str,
    ):
        if len(self.email_recipients) == 0:
            context.log.warning("No email recipients configured")
            return

        client = self.get_client()
        res = client.send_email(
            Destination={
                "ToAddresses": self.email_recipients,
            },
            Message={
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": subject,
                },
                "Body": {
                    "Html": {
                        "Charset": "UTF-8",
                        "Data": html,
                    },
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": text,
                    },
                },
            },
            Source=self.sender_email,
            ConfigurationSetName=self.configuration_set,
        )
        context.log.info(f"{res['MessageId']=}")
