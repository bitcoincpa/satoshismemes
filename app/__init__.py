from flask import Flask
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET


s3 = boto3.client('s3', aws_access_key_id='AKIASDAIHF3AEIH6RTCF', aws_secret_access_key='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')

app = Flask(__name__, static_url_path="/static", static_folder="static")


from app import views