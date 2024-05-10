import boto3
from django.conf import settings


def upload_file_to_s3(file_object):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_name = file_object.name

    try:
        s3.upload_fileobj(file_object, bucket_name, file_name)
    except Exception as e:
        print("Error uploading file to S3:", str(e))