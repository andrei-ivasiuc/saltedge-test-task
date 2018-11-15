Test Task for Saltedge by Andrei Ivasiuc
----------------------------------------

Requirements:

* Python == 2.7
* Mysql >= 5.0 

Structure:

* requirements.txt - Python package requirements
* schema.sql - MYSQL schema
* db_credentials.json - Database credentials
* app.py - App executable
* model.py - Class used for DB manipulations
* templates - HTML templates
* static - Static files, served by Flask

Installation:

`pip install -r requirements.txt`

DB Connection:

Update `db_credentials.json` to match your local env.

To run server:

`flask run`
