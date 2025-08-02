import pytest
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.bike_sharing import prepare_data
import os
import boto3
import logging

#boto3.set_stream_logger('botocore', level='DEBUG')

TESTS_BUCKET_NAME = os.getenv("BUCKET_NAME") + "-tests"

@pytest.fixture
def clear_bucket():
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = s3.list_objects_v2(Bucket=TESTS_BUCKET_NAME)

    if "Contents" in response:
        for item in response["Contents"]:
            s3.delete_object(Bucket=TESTS_BUCKET_NAME, Key=item["Key"])
    logging.info("bucket cleared")

@pytest.fixture
def prepare_data_fixture(clear_bucket):
    return prepare_data(data_bucket_name=TESTS_BUCKET_NAME)

@pytest.fixture
def get_bucket_keys(prepare_data_fixture):
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = s3.list_objects_v2(Bucket=TESTS_BUCKET_NAME)
    if "Contents" in response:
        return {item["Key"]: item["Size"] for item in response["Contents"]}
    return {}


def test_prepare_data_files(get_bucket_keys): 
    keys = get_bucket_keys
    
    expected_keys = ["train_x.csv", "test_x.csv", "train_y.csv", "test_y.csv"]

    assert set(keys.keys()) == set(expected_keys)

def test_prepare_data_file_sizes(get_bucket_keys): 
    keys = get_bucket_keys
    
    assert all(size > 0 for size in keys.values())
