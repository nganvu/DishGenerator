from flask import Flask, render_template, flash, request
from wtforms import Form, BooleanField, IntegerField, TextField, TextAreaField, validators, StringField, SubmitField
import pymysql
from google import google
from pprint import pprint

import sys  
reload(sys)  
sys.setdefaultencoding("utf8")

app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "7d441f27d441f27567d441f2b6176a"

timing = {"breakfast", "brunch", "lunch", "dinner", "dessert"}

class ReusableForm(Form):
    name = TextField(validators=[validators.Optional()])
    ingredients = TextField(validators=[validators.Optional()])
    occasions = TextField(validators=[validators.Optional()])
    breakfast = BooleanField()
    brunch = BooleanField()
    lunch = BooleanField()
    dinner = BooleanField()
    dessert = BooleanField()
    calories = IntegerField()
    submit = SubmitField()

class Database:
    def __init__(self):
        host = "localhost"
        user = "envy"
        password = "abc"
        db = "FoodApp"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def query_database(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result
    
    def add_google_link(self, result):
        for row in result:
            links = google.search(row["title"])
            if len(links) >= 1:
                row["link"] = links[0]
        return result

@app.route("/", methods=["GET", "POST"])
def employees():

    def db_query(query):
        db = Database()
        res = db.query_database(query)
        res = db.add_google_link(res)
        return res
    
    form = ReusableForm(request.form)
    
    res = {}
    query = ""

    if request.method == "POST":
        query = \
            "select main.title, nutrition.calories from main\
            inner join timing on main.dish_idx = timing.dish_idx\
            inner join ingredient on main.dish_idx = ingredient.dish_idx\
            inner join occasion on main.dish_idx = occasion.dish_idx\
            inner join nutrition on main.dish_idx = occasion.dish_idx"

        pprint(vars(request))

        name = request.form["name"]
        if name:
            query += " and main.title like '%{}%'".format(name)

        ingredients = request.form["ingredients"]
        if ingredients:
            ingredients = ingredients.split(',')
            ingredients = [x.strip() for x in ingredients]
            for ingredient in ingredients:
                query += " and ingredient.`{}` = true".format(ingredient)

        occasions = request.form["occasions"]
        if occasions:
            occasions = [x.strip() for x in occasions.split(',')]
            for occasion in occasions:
                query += " and occasion.`{}` = true".format(occasion)

        for time in timing:
            if time in request.form:
                query += " and timing.`{}` = true".format(time)

        calories = request.form["calories"]
        if calories:
            query += " and nutrition.calories < {}".format(calories)

        query += " order by rand() limit 3"

        if form.validate():
            res = db_query(query)
        else:
            flash("All the form fields are required. ")
    return render_template("index.html", query=query,
        form=form, result=res, content_type="application/json")

