import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv(".env")

celery = Celery('tasks')
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
