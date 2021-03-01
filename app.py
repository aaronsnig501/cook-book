import os
from os.path import join, dirname
import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from dotenv import load_dotenv

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

        user = {"username": username, "email": email, "password": str(hashed)}

        mongo.db.users.insert_one(user)

        session["user"] = user["username"]
        print(session)

        return redirect(url_for("recipes"))
    return render_template("accounts/register.html")


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