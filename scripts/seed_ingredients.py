from app import db, Ingredient
from flask import Flask

# Only needed if you get "working outside application context" errors
from app import app

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
