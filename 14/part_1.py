from collections import defaultdict


class RecipeBook:
    def __init__(self, raw_data):
        self.recipes = defaultdict(list)
        self.make_recipes(raw_data)

    def __getitem__(self, recipe):
        return self.recipes[recipe]

    def make_recipes(self, data):
        split_data = [line.strip().split('=>') for line in data.split('\n') if line.strip()]

        for ingredients, result in split_data:
            parsed_result = self.create_ingredient(result)
            for ingredient in ingredients.split(','):
                self.recipes[parsed_result].append(self.create_ingredient(ingredient))

    @staticmethod
    def create_ingredient(unparsed_ingredient):
        parsed = [item.strip() for item in unparsed_ingredient.split(' ') if item.strip()]
        return Ingredient(parsed[1].replace(' ', ''), int(parsed[0]))

    def get_recipe(self, ingredient):
        for recipe in self.recipes:
            if recipe.ingredient == ingredient:
                return recipes[recipe]

    def make_recipe(self, item):
        recipe = self.get_recipe(item)
        running_counts = defaultdict(int)

        for ingredient in recipe:
            running_counts[ingredient.ingredient] += ingredient.amount
            self.make_recipe(ingredient.ingredient)

        return running_counts


class Ingredient:
    def __init__(self, ingredient, amount):
        self.ingredient = ingredient
        self.amount = amount

    def __repr__(self):
        return f"{self.amount} {self.ingredient}"


if __name__ == '__main__':
    test_input_1 = """
    10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL
    """

    recipes = RecipeBook(test_input_1)
    recipes.make_recipe('FUEL')

