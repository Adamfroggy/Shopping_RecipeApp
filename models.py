class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = [Ingredient(*ingredient)
                            # List of Ingredient objects
                            for ingredient in ingredients]
        self.instructions = instructions


class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
