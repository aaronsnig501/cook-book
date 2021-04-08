import os
from os.path import join, dirname
import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from utils.recipe import recipe_parser
from utils.decorators import requires_owner

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.errorhandler(403)
def forbidden(e):
    """Forbidden handler

    Render `403` template to users if they try to modify recipes they don't own

    Returns:
        403 template
    """
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def not_found(e):
    """Resource not found handler

    Render `404` template to users if they try to access a resource that doesn't exist

    Returns:
        404 template
    """
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    """Resource not found handler

    Render `500` template to users if an unhandled error causes an internal server error

    Returns:
        500 template
    """
    return render_template("errors/500.html"), 500


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

    Handle the register view.

    If the request is a POST, the form will be parsed and a password will be generated
    using `bcrypt`. That user will be added to the database and added to the session.
    The user will then be redirected to `/recipes`

    Returns:
    - GET: The `register.html` file
    - POST: Redirects to `/recipes`
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
    """Login view

    Handles the login view.

    If the request is a POST, the form will be parsed and `bcrypt` will check that the
    password matches the user's password. If so, the user will be added to the session
    and redirected to `/recipes`

    Returns:
    - GET: The `login.html` file
    - POST: Redirects to `/recipes`
    """
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
    """Logout view

    Clears the session and redirects the user to the login page

    Returns:
    - Redirect to `/login`
    """
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    """Profile view

    Get all of the currently logged in user's recipes and return them along with the
    `profile.html`

    Returns:
    - Renders the `profile.html` file with the user's recipes
    """
    recipes = mongo.db.recipes.find({"created_by": session["user"]})
    return render_template("accounts/profile.html", recipes=recipes)


@app.route("/recipes")
def recipes():
    """Recipes view

    Handle the recipes route. This will get a list of the recipes to present to
    users.

    Returns:
    - The `recipes.html` containing the recipes
    """
    recipes = mongo.db.recipes.find()
    return render_template("recipes/list.html", recipes=recipes)


@app.route("/recipe/<id>")
def recipe(id):
    """Recipe

    Gets an individual recipe based on the ID of the recipe that the user click on
    and return it along with the `details.html` file. In addition to rendering the item,
    the recipes number of views is also increased by one

    Returns:
    - Renders the `details.html` with the recipe data
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    mongo.db.recipes.update(
        {"_id": ObjectId(id)}, {"$set": {"views": recipe["views"] + 1}}
    )
    return render_template("recipes/details.html", recipe=recipe)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    """Add recipe

    Renders the `create.html` file if request is a GET, and parses the form data if
    method is a POST. This will insert the new recipe into the database.

    Returns:
    - GET: Renders the `create.html` page
    - POST: Redirect to `/recipes`
    """
    if request.method == "POST":
        recipe = recipe_parser(dict(request.form), session["user"])

        mongo.db.recipes.insert_one(recipe)

        return redirect(url_for("recipes"))
    return render_template("recipes/create.html")


@app.route("/edit-recipe/<id>", methods=["GET", "POST"])
@requires_owner(mongo)
def edit_recipe(id):
    """Edit recipe

    Get the recipe to be updated to provide the default data in the form. If method
    is POST, parse the data and commit the updated data to the database.

    Returns:
    - GET: Render `edit.html`
    - POST: Redirect to `/recipes`
    """
    existing_recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        recipe = recipe_parser(dict(request.form), session["user"])
        mongo.db.recipes.update({"_id": ObjectId(id)}, recipe)
        return redirect(url_for("recipes"))

    return render_template("recipes/edit.html", recipe=existing_recipe)


@app.route("/delete-recipe/<id>")
@requires_owner(mongo)
def delete_recipe(id):
    """Delete recipe

    Delete the recipe with the provided ID.

    Returns:
    - Redirects to `/recipes`
    """
    mongo.db.recipes.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("recipes"))


@app.route("/search", methods=["POST"])
def search():
    """Search view

    Handles the search request. The index on Mongo is set up as a text index across the
    name, description, ingredients and steps fields. Any text provided by the search form
    will check those fields for any matching text and return the results

    Returns:
        Renders the `recipes/list.html` template with the search results
    """
    query = request.form.get("query", None)
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template("recipes/list.html", recipes=recipes)
