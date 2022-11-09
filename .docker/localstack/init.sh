#!/usr/bin/env bash

echo "localstack setup!"

echo "Creating S3 bucket reports"
awslocal s3 mb s3://client-reports

echo "setup finished!"
