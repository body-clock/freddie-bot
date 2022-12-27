import os
import boto3

aws_access_key_id = os.environ['AWS_ID']
aws_secret_access_key = os.environ['AWS_SECRET']
s3_client = s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)


def download_csv_from_aws(bucket_name, file_name, file_path):
    """Download a CSV from AWS to a path"""
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
    s3_resource.Bucket(bucket_name).download_file(file_name, file_path)
    return file_path


def upload_image_to_s3(image, bucket, image_name):
    """Upload image to s3 bucket"""
    s3_client.upload_fileobj(image, bucket, image_name)


def download_image_from_s3(bucket, image_name, download_path):
    """Download image into lambda /tmp/ directory"""
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
    s3_resource.Bucket(bucket).download_file(image_name, download_path)


def delete_image_from_s3(bucket, image_name):
    """Delete image from s3 bucket"""
    s3.delete_object(Bucket=bucket, Key=image_name)
