from datetime import datetime


def _parse_ingredients(recipe):
    """Parse ingredients

    The ingredients come in from the form as normal key value pairs. This needs to be
    changed so that the ingredients can be stored as the following data structure.

    [
        {
            name: "Chicken",
            quantity: "400",
            measurement: "grams"
        }
    ]

    Args:
        recipe (dict): The recipe form data

    Returns:
        list<dict>: The ingredients in the required format
        dict: The dict of all of the ingredients
    """
    ingredients = []
    group_counter = 1
    counter = 0

    filtered_dict = {k: v for k, v in recipe.items() if "ingredient" in k}
    ingredient = {}

    for key, value in filtered_dict.items():
        if not value:
            continue

        elif key == f"ingredient{group_counter}":
            ingredient["name"] = value

        elif key == f"ingredientQuantity{group_counter}":
            ingredient["quantity"] = value

        elif key == f"ingredientMeasurement{group_counter}":
            ingredient["measurement"] = value

        counter += 1
        if counter % 3 == 0:
            ingredients.append(ingredient)
            ingredient = {}
            group_counter += 1

    return ingredients, filtered_dict


def _parse_steps(recipe):
    """Parse steps

    The steps come in from the form as normal key value pairs. This needs to be
    changed so that the ingredients can be stored as the following data structure.

    [
        "Dice chicken",
        "Cook chicken until brown"
    ]

    Args:
        recipe (dict): The recipe form data

    Returns:
        list<str>: The steps in the required format
        dict: The dict of all of the steps
    """
    steps = []

    filtered_dict = {k: v for k, v in recipe.items() if "step" in k}

    for key, value in filtered_dict.items():
        if value:
            steps.append(value)

    return steps, filtered_dict


def recipe_parser(recipe, user):
    """Recipe parser

    Bundles up the information retrieved from the request, parses it and
    strips away the excess information.

    Args:
        recipe (dict): The recipe information provided by the HTML form
        user (str): The username of the currently logged in user

    Returns:
        dict: The newly generated recipe data structure
    """
    recipe["ingredients"], filtered_ingredients = _parse_ingredients(recipe)
    recipe["steps"], filtered_steps = _parse_steps(recipe)
    recipe["created_by"] = user
    recipe["created_at"] = datetime.now()
    recipe["views"] = 0
    recipe["likes"] = 0

    for key, _ in filtered_ingredients.items():
        if key in recipe:
            del recipe[key]

    for key, _ in filtered_steps.items():
        if key in recipe:
            del recipe[key]

    return recipe