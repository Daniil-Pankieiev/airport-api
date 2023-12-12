# Airport API 

API service for odering tickets and tracking flights.

## Installing using GitHub
Install PostgresSQL and create db.

1. Clone the repository:
```bash
git clone https://github.com/Daniil-Pankieiev/airport-api
```
2. Navigate to the project directory:
```bash
cd airport_api
```
3. Switch to the develop branch:
```bash
git checkout develop
```
4. Create a virtual environment:
```bash
python -m venv venv
```
5. Activate the virtual environment:

On macOS and Linux:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```
6. Install project dependencies:
```bash
pip install -r requirements.txt
```
7. Copy .env.sample to .env and populate it with all required data.
8. Run database migrations:
```bash
python manage.py migrate
```
9. Optional: If you want to load your database with some data, use:
```bash
python manage.py loaddata db_airport_data.json
```
10. Start the development server:
```bash
python manage.py runserver
```
