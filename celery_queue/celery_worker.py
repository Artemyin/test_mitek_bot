import os
from celery import Celery
from dotenv import load_dotenv
import boto3
import requests
from audio_converter import convert_ogg_to_wav
from face_detector import detect_face
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

@celery.task(name="process_photo")
def process_photo(link, name, user_id):
    download_file(link, name)
    detected = detect_face(name)
    if detected:
        new_name = str(generate_random_name(12)) + ".jpeg"
        s3_name = f"'photos'/{user_id}/{new_name}"
        s3.upload_file(name, bucket_name, s3_name)
        result = json.loads('{{"result": "{0}"}}'.format(new_name))
    else:
        result = json.loads('{{"result": {0}}}'.format(0))
    os.remove(name)
    return result

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
