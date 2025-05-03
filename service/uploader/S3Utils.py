import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
import os


load_dotenv()


def getFileUploadURL(bucket_name, file_name, region):
    # Construct the S3 URL
    s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_name}"
    return s3_url


def fetch_s3_configs():
    config = {
        "bucket_name": os.getenv("S3_BUCKET_NAME"),
        "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region": os.getenv("AWS_REGION", "us-east-1"),
    }
    return config


def uploadToS3(file_path, bucket_name, s3_file_key, access_key, secret_key, region='us-east-1'):
    try:
        # Initialize S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        # Upload file to S3
        s3.upload_file(file_path, bucket_name, s3_file_key)
        return True

    except FileNotFoundError:
        print("❌ File not found.")
    except NoCredentialsError:
        print("❌ Invalid AWS credentials.")
    except ClientError as e:
        print(f"❌ AWS Client Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

    return False
