import os
import logging
import boto3


logging.info("init-s3.py script launch")

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
s3.create_bucket(Bucket=os.getenv("BUCKET_NAME"))
