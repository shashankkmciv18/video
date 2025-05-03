import os

from service.uploader.S3Utils import uploadToS3, getFileUploadURL, fetch_s3_configs


class S3UploaderService:
    def __init__(self):
        self.config = fetch_s3_configs()

    def upload_file_to_s3(self, file_path):
        s3_config = self.config
        bucket_name = s3_config["bucket_name"]
        access_key = s3_config["access_key"]
        secret_key = s3_config["secret_key"]
        region = s3_config["region"]

        # Generate S3 file key
        file_name = os.path.basename(file_path)
        s3_file_key = f"videos/{file_name}"

        # Upload to S3
        success = uploadToS3(file_path, bucket_name, s3_file_key, access_key, secret_key, region)

        if success:
            return getFileUploadURL(bucket_name, s3_file_key, region)
        else:
            raise Exception("Failed to upload video to S3.")
