# Usage
* Navigate to the project directory, then execute the following command line to import the database:
```
gunzip < FoodApp.sql.gz  | mysql -u [user] -p FoodApp
```
Enter password if requested.
* Inside the file app.py, change the "user" and "password" in class Database to your username and password.
* To run flask app, in the project directory, execute the following command lines:
```
export FLASK_APP=app.py
python -m flask run
```
The export command is only necessary if you are running the app for the first time.
* Go to http://127.0.0.1:5000/ to see the app
