from flask import Flask

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, Ingredient, app

# List of common ingredients you want to preload
ingredient_names = [
    "Flour",
    "Sugar",
    "Butter",
    "Eggs",
    "Milk",
    "Baking Powder",
    "Chocolate",
    "Salt",
    "Yeast",
    "Vanilla Extract"
]

def seed_ingredients():
    with app.app_context():
        for name in ingredient_names:
            existing = Ingredient.query.filter_by(name=name).first()
            if not existing:
                ingredient = Ingredient(name=name)
                db.session.add(ingredient)
        db.session.commit()
        print("Ingredients loaded successfully! 🌟")

if __name__ == "__main__":
    seed_ingredients()
