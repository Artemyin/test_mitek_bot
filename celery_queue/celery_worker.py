import os
from celery import Celery
from dotenv import load_dotenv
import boto3
import requests
from audio_converter import convert_ogg_to_wav
import json

import random
import string


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
def process_photo(link, name, user_id):
    payload = {
        "url": link,
        "accuracy_boost": 3
    }
    response = requests.post(url, json=payload, headers=headers)
    faces = response.json().get("detected_faces")
    if faces and faces[0].get("Probability") > 90:
        download_file(link, name)
        new_name = str(generate_random_name(12)) + ".jpeg"
        s3_name = f"'photos'/{user_id}/{new_name}"
        s3.upload_file(name, bucket_name, s3_name)
        os.remove(name)
        return json.loads('{{"result": "{0}"}}'.format(new_name))
    return json.loads('{{"result": {0}}}'.format(0))

@celery.task(name="process_voice")
def process_voice(link, name, user_id):
    download_file(link, name)
    new_name = str(generate_random_name(12))
    print("try to convert")
    convert_ogg_to_wav(name, new_name)
    print("converted")

    s3_name = f"'voices'/{user_id}/{new_name.strip() + '.wav'}"
    s3.upload_file(new_name, bucket_name, s3_name)
    os.remove(name)
    os.remove(new_name)
    response = '{{"result": "{0}"}}'.format(new_name + '.wav')
    return json.loads(response)


def download_file(link, name):
    response = requests.get(link)
    if response.status_code == 200:
        with open(name, "wb") as f:
            f.write(response.content)
            print("File downloaded successfully!")
    else:
        print(f"Error downloading file. Status code: {response.status_code}")


def generate_random_name(length):
    return ''.join(random.choices(string.ascii_letters, k=length))
