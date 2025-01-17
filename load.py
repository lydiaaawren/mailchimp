import zipfile  # For handling .zip files
import gzip     # For handling .gz files
import os       # For file/directory operations
import shutil   # For file operations like copying
from pathlib import Path  # For modern path handling
import tempfile # For creating temporary directories
import boto3    # For push to AWS s3
from dotenv import load_dotenv # Reads .env file
from botocore.client import ClientError

# Load .env file
load_dotenv()

# Set up AWS credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
bucket_name = os.getenv('AWS_BUCKET_NAME')
aws_kms_key = os.getenv('AWS_KMS_KEY')

# sort client and credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

local_folder ='./data'
s3_folder = 'python-upload'

for root, dirs, files in os.walk(local_folder):
    for file in files:
        # only get jsons
        if not file.endswith(".json"):
            continue
        # make the local path
        local_path = os.path.join(root, file)
        # make the S3 path (keep folder structure)
        relative_path = os.path.relpath(local_path, local_folder)
        s3_path = os.path.join(s3_folder, relative_path).replace("\\", "/")
        # upload
        print(f"Uploading {local_path} to s3://{bucket_name}/{s3_path}")
        s3_client.upload_file(local_path, bucket_name, s3_path)

for root, dirs, files in os.walk(local_folder):
    for file in files:
        # only delete jsons
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            print(f"Deleting: {file_path}")
            os.remove(file_path) 