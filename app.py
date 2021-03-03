import os
from os.path import join, dirname
from datetime import datetime
import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from utils.recipe import parse_ingredients, parse_steps

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register view

    Handle the register view

    Returns:
    - The `register.html` file
    """
    if request.method == "POST":
        username = request.form.get("username", None)
        email = request.form.get("email", None)
        password = request.form.get("password", None)

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        user = {"username": username, "email": email, "password": hashed}

        mongo.db.users.insert_one(user)

        session["user"] = user["username"]
        return redirect(url_for("recipes"))
    return render_template("accounts/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", None)
        password = request.form.get("password", None)

        user = mongo.db.users.find_one({"email": email})

        if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            session["user"] = user["username"]
            return redirect(url_for("recipes"))
    return render_template("accounts/login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    recipes = mongo.db.recipes.find({"created_by": session["user"]})
    return render_template("accounts/profile.html", recipes=recipes)


@app.route("/recipes")
def recipes():
    """Recipe view

    Handle the recipe route. This will get a list of the recipes to present to
    users.

    Returns:
    - The `recipes.html` containing the recipes
    """
    recipes = mongo.db.recipes.find()
    return render_template("recipes/list.html", recipes=recipes)


@app.route("/recipe/<id>")
def recipe(id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    return render_template("recipes/details.html", recipe=recipe)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = dict(request.form)
        recipe["ingredients"] = parse_ingredients(recipe)
        recipe["steps"] = parse_steps(recipe)
        recipe["created_by"] = session["user"]
        recipe["created_at"] = datetime.now()
        recipe["views"] = 0
        recipe["likes"] = 0

        mongo.db.recipes.insert_one(recipe)

        return redirect(url_for("recipes"))
    return render_template("recipes/create.html")