def parse_ingredients(recipe):
    ingredients = []
    group_counter = 1
    counter = 0

    filtered_dict = {k: v for k, v in recipe.items() if "ingredient" in k}
    ingredient = {}

    for key, value in filtered_dict.items():
        if key == f"ingredient{group_counter}":
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


def parse_steps(recipe):
    steps = []

    filtered_dict = {k: v for k, v in recipe.items() if "ingredient" in k}
    step = {}

    for key, value in filtered_dict.items():
        step[key] = value

        steps.append(step)

    return steps, filtered_dict
