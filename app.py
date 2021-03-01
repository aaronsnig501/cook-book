import os
from os.path import join, dirname
from flask import Flask, render_template
from flask_pymongo import PyMongo
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.route("/")
def index():
    """Index view

    Handle the index route.

    Returns:
    - The `index.html` file
    """
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    """Recipe view

    Handle the recipe route. This will get a list of the recipes to present to
    users.

    Returns:
    - The `recipes.html` containing the recipes
    """
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)