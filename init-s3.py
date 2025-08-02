import logging
import os

import boto3

logging.info("init-s3.py script launch. Going to create s3 buckets.")

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)
s3.create_bucket(Bucket="mlflow-bucket")
s3.create_bucket(Bucket=os.environ.get("BUCKET_NAME"))
s3.create_bucket(Bucket=os.environ.get("BUCKET_NAME") + "-tests")
logging.info("Three buckets are created (mlflow, main and test).")
