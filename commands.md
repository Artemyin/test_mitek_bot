1. bot download voice and photos
2. add env variables
3. add docker, docker compose with postgres and pg admin
docker-compose up -d --build
4. add models.py
5. add and set-up alembic
alembic init alembic
docker-compose run app alembic revision --autogenerate -m "New Migration"  # create migration instruction
docker-compose run app alembic upgrade head  # apply migration to DB
6. create crud
7. 
