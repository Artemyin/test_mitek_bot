import os
import time

from celery import Celery
from dotenv import load_dotenv

import requests
from audio_converter import convert_ogg_to_wav

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


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
def process_voice(voice):
    convert_ogg_to_wav(voice, output_file, sample_rate=16000)
    return

