Stack:
python-telegram-bot
PostgreSQL with pgadmin4 and alembic for migration
Celery with Redis and Flower
Face recognition: rapidapi.com
Audio: pydub with ffmpeg
S3 for file storage.

service app: handle requests from tg and send tasks to celery workers, gets file names and add new entry to DB.
celery_queue: downloads files process them and uploads to s3 bucket

