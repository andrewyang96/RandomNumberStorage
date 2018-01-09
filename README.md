# RandomNumberStorage
Test application using AWS Lambda, SES, and RDS (Postgres). Deployed with [python-lambda](https://github.com/nficano/python-lambda).

## Initialization
Make an AWS Lambda function named "random_numbers". Set its handler to `service.handler` and save changes. Then, verify an email on Amazon SES.

## Environment variables
Run `cp config.json.example config.json` and fill in the fields.

## Development
Download [awslambda-psycopg2](https://github.com/jkehler/awslambda-psycopg2) and copy the `psycopg2-3.6` into the project directory. Rename it to `psycopg2`.

## Deployment
Run `make deploy`. Configure a CloudWatch Event and its schedule expression, and save changes. Set the "ENABLE_EMAIL" environment variable in the Lambda console and add the "AmazonSESFullAccess" permission to the execution role to enable email sending.
