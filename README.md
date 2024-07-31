# dagster-notif-template

This is a barebones Dagster template that includes code for pipeline failure notifications via Slack and email. AWS SES
is used here as the email service; adjust any code and variables as needed if you're using a different email service (
i.e. Sendgrid, SMTP).

## Prerequisites

- [ ] Python 3.11
- [ ] Poetry

## Setup

```shell
poetry install --no-root --with dev
```

Copy the contents of `.env.example` into a new file named `.env` and supply the needed values.

## Running locally

```shell
poetry run dagster dev -p 3000
```
