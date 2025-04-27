import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, Recipe, Ingredient, app

# Some sample recipes
sample_recipes = [
    {
        "title": "Classic Pancakes",
        "ingredient_name": "Flour",
        "instructions": "Mix flour, eggs, milk, and baking powder. Cook on a skillet until golden brown."
    },
    {
        "title": "Chocolate Chip Cookies",
        "ingredient_name": "Chocolate",
        "instructions": "Mix flour, sugar, butter, chocolate chips. Bake until golden."
    },
    {
        "title": "Scrambled Eggs",
        "ingredient_name": "Eggs",
        "instructions": "Whisk eggs, season with salt, cook gently over low heat."
    }
]

def seed_recipes():
    with app.app_context():
        for r in sample_recipes:
            ingredient = Ingredient.query.filter_by(name=r["ingredient_name"]).first()
            if ingredient:
                recipe = Recipe(
                    title=r["title"],
                    instructions=r["instructions"],
                    ingredient_id=ingredient.id
                )
                db.session.add(recipe)
        db.session.commit()
        print("Sample recipes added successfully! 🍩")

if __name__ == "__main__":
    seed_recipes()
