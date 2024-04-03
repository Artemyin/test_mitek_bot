import os
import time

from celery import Celery
from dotenv import load_dotenv

import requests

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


url = "https://face-detection6.p.rapidapi.com/img/face-age-gender"
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "6f65d4f1f0msh5384163a85e65f5p12cfb9jsn6afd2199383f",
	"X-RapidAPI-Host": "face-detection6.p.rapidapi.com"
}

@celery.task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c

@celery.task(name="process_photo")
def process_photo(photo):
    payload = {
        "url": photo,
        "accuracy_boost": 3
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


