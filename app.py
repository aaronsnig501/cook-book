import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


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
    recipes = [
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
        {
            "name": "Chicken Curry",
            "preparation_time": 10,
            "ingredients": [{"name": "Chicken", "quantity": 400, "measurement": "g"}],
            "image": "https://www.cookingclassy.com/wp-content/uploads/2018/08/chicken-curry-11-768x1152.jpg"
        },
    ]
    return render_template("recipes.html", recipes=recipes)