# Airport-API-Service 

Welcome to the Airport Service API! Best solution for managing flight orders, routes, planes, tickets ordering and more. Airport Service API suites both developers integrating airport management infrastructure or airline company in need of efficient system to handle reservations and flights .

___

## Airport Service DB Structure
![db_structure.png](readme%2Fdb_structure.png)
## Features
* JWT Authentication
* Email-Based Authentication
* Admin panel
* Throttling Mechanism
* API documentation
* Creating airplane with Image
* Filtering for Flights and Routs
* Managing orders and tickets
* Implement a new permission class 
___

## Prerequisites
Following prerequisites need to be installed on your system:

- **Docker:** You can download and install Docker from the official website: https://www.docker.com/.
- **ModHeader:** You can download and install ModHeader from the official website: https://modheader.com/.


## How to use

### Installing using GitHub

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
<details>
<summary>Parameters for .env file:</summary>

- **POSTGRES_DB**: `Name of your DB`
- **POSTGRES_USER**: `Name of your user for DB`
- **POSTGRES_PASSWORD**: `Your password in DB`
- **POSTGRES_HOST** `Host of your DB`
</details>

#### Working with SQLite
1. Run database migrations:
```bash
python manage.py migrate
```
2. Optional: If you want to prepopulate your database with some data, use:
```bash
python manage.py loaddata db_airport_data.json
```
3. Start the development server:
```bash
python manage.py runserver
```

#### Working with Docker and PostgreSQL
Docker should be installed.

1. Use Docker Compose to build the API's Docker container:
``` 
docker-compose build
```

2. Run container:
```
docker-compose up --build
```

##### When API project use:

You need to generate access token. Do to: ``127.0.0.1:8000/api/user/token``

To use servie as admin enter following credentials:
- login: ``admin@admin.com``
- password: ``secretpassword``


After logging in with provided credentials you will receive two tokens: access token and refresh token.
Add new request headed and enter information:

Name: ``Authorization``

Value: ``Bearer_space_*your_access_token*`` 

Access token example. ``Bearer dmwkejeowk.ewkjeoqdowkjefowfejwefjwef.efhnwefowhefojw``

![ModHeader.png](readme%2FModHeader.png)
Go to ``127.0.0.1:8000/api/airport/`` and discover all hidden gems

## Contributing
Feel free to contribute to these enhancements, and let's make our Airport Service API even better!
## Conclusion

Thank you for using the Airport Service API! 
