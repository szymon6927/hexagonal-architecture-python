from typing import Any, Mapping

from mypy_boto3_s3.client import S3Client
from mypy_boto3_ses.client import SESClient
from mypy_boto3_sns.client import SNSClient

MongoDocument = Mapping[str, Any]
SNSSdkClient = SNSClient
S3SdkClient = S3Client
SESSdkClient = SESClient
