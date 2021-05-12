Calculating distances service
=============================

Developer environment installation
----------------------------------

 * Clone project repo:

* Setup PostgreSQL

https://www.postgresql.org/download/
   
create database:
   
psql `CREATE DATABASE d_test;`

   OR change database name in settings.py 
    'postgresql://postgres:postgres@localhost:5432/<your_database_name>'

 * Setup python and virtual environment:
   
   install python 3.8

  ` cd ./dokka_test_vd`

   `python3 -m venv /ve`

   `source ve/bin/activate`

  ` pip install -r requirements.txt`
   
 
* Setup and run Flask:
  
`flask db upgrade`
  
  `esport FLASK_APP=apps.api.views`
  
  `flask run`
  
* Run Celery worker:

`celery worker  --app=apps.services.tasks --loglevel=info --logfile=logs.celery.log`
  
* Run Celery Flower (if needed):

`flower --app=apps.services.tasks --port=5555 --broker=redis://localhost:6379`

 
Testing
-------

* run POST request:

`curl -H "Content-T-data" -H "Authorization: Basic YWRtaW46QWRtaW4=" -F "file=@locations.csv" http://127.0.0.1:5000/api/calculateDistances
 `
 
 example file locations.csv:

 ![img_1.png](img_1.png)
 
 Point,Latitude,Longitude

A,50.448069,30.5194453

B,50.448616,30.5116673

C,50.913788,34.7828343

result should look like:

`{
  "status": "running",
  "task_id": "516c881b-62a0-48d0-8392-0ab0bfdb99a5"
}`

* run GET request to:
http://127.0.0.1:5000/api/getResult/<task_id>
  
where task_id - obtained on previous step

example:

  `curl -H "Authorization: Basic YWRtaW46QWRtaW4=" http://127.0.0.1:5000/api/getResult/d4153f4b-7f93-45bf-9892-205fd7183d42`

