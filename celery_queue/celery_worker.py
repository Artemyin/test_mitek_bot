import os
import time
from pathlib import Path
from celery import Celery
from dotenv import load_dotenv
import boto3
import requests
from audio_converter import convert_ogg_to_wav

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
                  )
bucket_name = os.environ.get("BUCKET_NAME")

url = "https://face-detection6.p.rapidapi.com/img/face"
rapid_api_key = os.environ.get("RAPIDAPI_KEY")
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": rapid_api_key,
	"X-RapidAPI-Host": "face-detection6.p.rapidapi.com"
}

@celery.task(name="process_photo")
def process_photo(photo):
    payload = {
        "url": photo,
        "accuracy_boost": 3
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@celery.task(name="process_voice")
async def process_voice(file):
    voice_path = Path.cwd().joinpath("voices", file.file_unique_id)
    await file.download_to_drive(voice_path)
    convert_ogg_to_wav(voice_path, file.file_unique_id, sample_rate=16000)
    s3.upload_file(voice_path, bucket_name, file.file_unique_id)
    return True

