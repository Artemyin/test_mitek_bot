### Stack:
- Python-telegram-bot

- PostgreSQL with pgadmin4 and alembic for migration

- Celery with Redis and Flower

- Face recognition: rapidapi.com

- Audio: pydub with ffmpeg

- S3 for file storage.

### Services
- **service app**: handle requests from tg and send tasks to celery workers, gets file names and add new entry to DB.

- **celery_queue**: downloads files process them and uploads to s3 bucket

### instructions
to run project do following:
```
populte .env file in root folder, app/ and celery_queue/
```
```bash
$ docker-compose up -d --build
$ docker-compose exec app alembic upgrade head 
```
pgadmin - localhost:5050
```yaml
general:name: db
connection:host_name: db
maitenance database: postgres
username: postgres
password: password
```
flower - localhost:5556 

s3 bucket name - mitek-bucket

s3 location - eu-west-3
