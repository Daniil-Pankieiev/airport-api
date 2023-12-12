# Airport-API-Service
Api service for tracking flights written on DRF

# Installing using GitHub
Install PostgresSQL and create db

git clone https://github.com/Daniil-Pankieiev/airport-api
cd cinema_API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
create .env file, inside define variables from .env.sample

python manage.py migrate
python manage.py runserver

you can use command python manage.py loaddata db_airport_data.json to fill db 


# Getting access
create user via /api/user/register/
get access token via /api/user/token/
