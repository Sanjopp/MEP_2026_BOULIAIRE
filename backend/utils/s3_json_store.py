import json
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

# Environment variables
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_PREFIX = os.environ.get("S3_PREFIX", "")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

# Create S3 client (AWS S3 or S3-compatible, e.g. MinIO)
_s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
)


def _key(name: str) -> str:
    """Build full S3 object key with optional prefix."""
    return f"{S3_PREFIX}{name}"


def load_json(name: str, default: Any) -> Any:
    """
    Load a JSON object from S3.
    If the object does not exist or is invalid, return default.
    """
    if not S3_BUCKET:
        raise RuntimeError("S3_BUCKET is not set")

    try:
        response = _s3_client.get_object(
            Bucket=S3_BUCKET,
            Key=_key(name),
        )
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "NoSuchBucket"):
            return default
        raise
    except (json.JSONDecodeError, UnicodeDecodeError):
        return default


def save_json(name: str, data: Any) -> None:
    """
    Save a JSON object to S3.
    """
    if not S3_BUCKET:
        raise RuntimeError("S3_BUCKET is not set")

    _s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=_key(name),
        Body=json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json",
    )
