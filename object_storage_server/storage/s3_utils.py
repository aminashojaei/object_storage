import boto3
import logging
from botocore.exceptions import ClientError
from django.conf import settings

logging.basicConfig(level=logging.INFO)

BUCKET_NAME = 'webdev'
AWS_ACCESS_KEY_ID = 'cad70d91-4a59-41df-93e4-0013e5b5a6e6'
AWS_SECRET_ACCESS_KEY = 'be7021a93bbee56063b1bca7b2bba8faefacdeef780b270642eec622357a7a69'
AWS_ENDPOINT_URL='https://s3.ir-thr-at1.arvanstorage.ir'

class S3ResourceSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3ResourceSingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
     
            
        self.endpoint_url = AWS_ENDPOINT_URL
        self.aws_access_key_id = AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        try:
            self.s3_resource = boto3.resource(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )
        except Exception as exc:
            logging.error(exc)
            self.s3_resource = None
        self._initialized = True

    def get_resource(self):
        return self.s3_resource


def create_bucket(bucket_name):
    s3_resource = S3ResourceSingleton().get_resource()

    if s3_resource is None:
        return False

    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.create(ACL='public-read')  
        return True
    except ClientError as exc:
        logging.error(exc)
        return False


def upload_file(file, object_name):
    s3_resource = S3ResourceSingleton().get_resource()

    if s3_resource is None:
        return False

    try:
        bucket = s3_resource.Bucket(BUCKET_NAME)

        bucket.put_object(
            ACL='public-read',
            Body=file,
            Key=object_name
        )
        return True

    except ClientError as e:
        logging.error(e)
        return False


def objects_list():
    s3_resource = S3ResourceSingleton().get_resource()

    if s3_resource is None:
        return None

    try:
        bucket = s3_resource.Bucket(BUCKET_NAME)
        object_keys = []
        for obj in bucket.objects.all():
            logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")
            object_keys.append(obj.key)

        return object_keys

    except ClientError as e:
        logging.error(e)
        return None


def download_file(download_path, object_name):
    s3_resource = S3ResourceSingleton().get_resource()

    if s3_resource is None:
        return False
    try:
        # bucket
        bucket = s3_resource.Bucket(BUCKET_NAME)

        object_name = object_name
        download_path = download_path

        bucket.download_file(
            object_name,
            download_path
        )
        return True
    except ClientError as e:
        logging.error(e)
        return False


def delete_file(object_id):
    s3_resource = S3ResourceSingleton().get_resource()

    if s3_resource is None:
        return False
    try:
        bucket = s3_resource.Bucket(BUCKET_NAME)
        object = bucket.Object(object_id)

        response = object.delete()
        print(response)
        return True
    except ClientError as e:
        logging.error(e)
        return False
    
