from functools import update_wrapper
from flask import session, abort, redirect, url_for
from bson.objectid import ObjectId


def requires_owner(mongo):
    """Requires owner

    This decorator is used to ensure that only the creator of a recipe can access that
    recipe. If the user is not the owner, a 403 will be thrown.

    Example usage::
        ```python
        from utils.decorators import requires_owner


        @app,route("/edit-recipe/<id>")
        @requires_owner
        def edit_recipe(id):
            # edit recipe code
        ```
    """

    def decorator(fn):
        def wrapped_function(*args, **kwargs):

            recipe = mongo.db.recipes.find_one({"_id": ObjectId(kwargs["id"])})

            if session["user"] != recipe["created_by"]:
                abort(403)
            return fn(*args, **kwargs)

        return update_wrapper(wrapped_function, fn)

    return decorator