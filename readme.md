Caloriecounter - Backend

This is a Django based project for a voice-based caloriecounter containing products featured in the USDA food database.

It features an API based on DRF, and an experimental pipeline for translating natural language into actions such as "I ate one onion", or "What is the number of calories in a bowl of yoghurt?"

Tests are included for the basic diary functionality. 
The 'voice' app, which manages a chat session with the user, and performs actions accordingly is not final.

# Requirements

 - Python 3.7
 - Postgres 10


# Installation 

To install the required dependencies simply run:

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

A Postgres database is required. The default credentials are inside local.py.
When running in production, environment values must be supplied for the SECRET_KEY as well as database credentials.
These can also be supplied in a .env file.

# Fixtures
For useful food data, I scraped the USDA database, and converted them to local format.
To import this data, use:

```sh
python manage.py loaddata fixtures/food.json
```
