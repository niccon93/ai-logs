
import boto3
from botocore.client import Config
from ..config import settings
def s3():
    return boto3.client("s3", endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY, aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION, config=Config(signature_version="s3v4"))
def ensure_bucket():
    c = s3()
    try: c.head_bucket(Bucket=settings.S3_BUCKET)
    except Exception: c.create_bucket(Bucket=settings.S3_BUCKET)
def upload_bytes(key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    ensure_bucket(); s3().put_object(Bucket=settings.S3_BUCKET, Key=key, Body=data, ContentType=content_type)
    return f"s3://{settings.S3_BUCKET}/{key}"
