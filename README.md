# Overall Framework
This project is developped in the framework of an education program as software developper in Python.

# Purpose
This web application offers the user to look for food items with better nutritional properties.
The main purpose of this project is to focus on password change by the user.

# Main Functionalities
- The user can create an account in order to get a better experience
- The user, be he anonymous or registered, is supposed to type in the name of a food item
- Then, the application looks for items of the same category with better nutritional properties
- The user can get more information on a selected product
- And he can subsequently record it
- The user can change his password
- The user can reset his password if it has been forgotten.

# This project is developped using :
- Python 3.8.1 
- Django 3.1.5
- Bootstrap 4

# Environments:
Different environments, named base, local and production have been developped.
To use papounet_super_diet in local mode, add the suffix:
**--settings papounet_super_diet.settings.local**
to your command line, be it for testing or running the server.

# Environment variables:
Environment variables (e.g. SECRET_KEY) are stored in a .env file, in the root folder of the project.
As they are not stored with the settings, you should create a .env file and store the SECRET_KEY over there.

# How to start the local server
- Create a virtual environment with python
- Install all the requirements, as listed in requirements.txt
- Make sure all the modules are installed.
- switch to papounet_diet module
- make migrations
- create a cache table
- run from the terminal: $ python manage.py runserver --settings papounet_super_diet.settings.local

## Testing:
### Commands for efficient testing
Using the Shell, type what the following command line, it will remove almost all irrelevant files.
As of 21.02.21 coverage rate reaches 90%

$ coverage run --omit='*/venv/*,*/tests/*,*/migrations/*,*/papounet_super_diet/tests.py,*/settings/*,*/manage.py,*/apps.py,*/admin.py'  manage.py test (+ local settings)

$ coverage report -m

### Where are the tests located ?
App customer: only basic testing as this module strictly follows Django guidelines.
App food_items:
- in module customer, iot check the routes
- in module openfoodfacts, iot check the import of data through their API
- in apps food_items and customer iot check the views and the queries.
- in papounet_diet, you will find the Selenium functional tests, with three user stories.

# Flake8 implementation
Depending on your Python alias, just type:
$ python -m flake8
A tox.ini file has been implemented and is to be found a the root of the project.
It excludes from Flake checking:
- all lines needed for in a Django project
- urls

# Architecture
Only the folders are depicted.
This program follows a Django standard architecture.

![Project Structure](support_documentation/architecture.png)

# Cache
This project uses a cache using the database.
Therefore, upon deployment, you should create a cache table, immediately after creating database migration.
e.g. : $ python3 manage.py createcachetable (don't forget to add the settings !)

# Deployment
This application owns different setting files in order to discriminate between local and deployment.

# Monitoring
This application offers following settings:
- Travis CI
- NewRelic
- Sentry

# Emails
This application is configured for using SendGrid


