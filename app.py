import os
from flask import Flask, render_template, request, redirect, url_for, flash, request, jsonify, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "bake"  

db = SQLAlchemy(app)

recipe_ingredient = db.Table('recipe_ingredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
)
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredient, backref='recipes')
    instructions = db.Column(db.Text, nullable=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)

 # automatically creates tables if not yet created
with app.app_context():
    db.create_all()

def process_ingredients(selected_ingredient_inputs):
    """Process selected ingredients: reuse existing or create new ones."""
    processed_ingredients = []
    for ing_input in selected_ingredient_inputs:
        ing_input = ing_input.strip()  # Trim spaces
        
        if ing_input.isdigit():
            # Existing ingredient
            ingredient = Ingredient.query.get(int(ing_input))
            if ingredient:
                processed_ingredients.append(ingredient)
        else:
            # New ingredient typed
            ing_input_lower = ing_input.lower()
            existing = Ingredient.query.filter(db.func.lower(Ingredient.name) == ing_input_lower).first()
            if existing:
                processed_ingredients.append(existing)
            else:
                new_ingredient = Ingredient(name=ing_input)
                db.session.add(new_ingredient)
                processed_ingredients.append(new_ingredient)
    return processed_ingredients

# home page
@app.route("/")
def home():
    recipes = Recipe.query.all() # display everything
    ingredients = Ingredient.query.all()
    return render_template("index.html", recipes=recipes, ingredients = ingredients)

# add recipe page
@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    # query alphabatically
    ingredients = Ingredient.query.order_by(Ingredient.name.asc()).all()
    
    if request.method == "POST":
        title = request.form["title"]
        selected_ingredient_inputs = request.form.getlist("ingredient_ids")
        instructions = request.form["instructions"]
        new_recipe = Recipe(title=title, instructions=instructions)
        new_recipe.ingredients.extend(process_ingredients(selected_ingredient_inputs))
        
        db.session.add(new_recipe)
        db.session.commit()
        flash("Recipe added successfully!")
        return redirect(url_for('home'))
    
    return render_template("add_recipe.html", ingredients = ingredients)

@app.route("/edit/<int:recipe_id>", methods=["POST"])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    recipe.title = request.form["title"]
    recipe.instructions = request.form["instructions"]
    selected_ingredient_inputs = request.form.getlist("ingredient_ids")

    recipe.ingredients = process_ingredients(selected_ingredient_inputs)

    db.session.commit()
    flash("Recipe updated successfully! 🎉")
    return redirect(url_for('view_recipe', recipe_id=recipe.id))


@app.route("/delete/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted successfully!")
    return redirect(url_for('home'))


# ------------------- Ingredients Related Routes
@app.route("/ingredients/")
@app.route("/ingredients/<letter>")
def all_ingredients(letter=None):
    if letter:
        ingredients = Ingredient.query.filter(
            Ingredient.name.ilike(f"{letter}%")
        ).order_by(Ingredient.name.asc()).all()
    else:
        ingredients = Ingredient.query.order_by(Ingredient.name.asc()).all()
    return render_template("ingredients.html", ingredients=ingredients, selected_letter=letter)

@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = Ingredient.query.order_by(Ingredient.name.asc()).all()
    return render_template("view_recipe.html", recipe=recipe, ingredients = ingredients)

@app.route("/add-ingredient", methods=["GET", "POST"])
def add_ingredient():
    if request.method == "POST":
        name = request.form["name"]
        new_ingredient = Ingredient(name=name)
        db.session.add(new_ingredient)
        db.session.commit()
        flash("Ingredient added successfully! 🥬")
        return redirect(url_for('add_ingredient'))
    
    ingredients = Ingredient.query.order_by(Ingredient.name.asc()).all()
    return render_template("add_ingredient.html", ingredients=ingredients)

@app.route("/edit-ingredient/<int:ingredient_id>", methods=["GET", "POST"])
def edit_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)

    if request.method == "POST":
        new_name = request.form["name"].strip()
        if new_name:
            ingredient.name = new_name
            db.session.commit()
            flash("Ingredient updated successfully! ✨")
            return redirect(url_for('add_ingredient'))

    return render_template("edit_ingredient.html", ingredient=ingredient)

@app.route("/delete-ingredient/<int:ingredient_id>", methods=["POST"])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)

    db.session.delete(ingredient)
    db.session.commit()
    flash("Ingredient deleted successfully! 🗑️")
    return redirect(url_for('add_ingredient'))

@app.route("/recipes")
def recipes():
    recipes = Recipe.query.all() # display everything
    return render_template("recipes.html", recipes=recipes)

@app.route("/populate_ingredients")
def populate_ingredients():
    common_ingredients = [
        "All-purpose flour", "Baking powder", "Baking soda", "Cornstarch", "Cocoa powder",
        "Powdered sugar", "Granulated sugar", "Brown sugar",
        "Butter", "Unsalted butter", "Margarine", "Vegetable oil", "Coconut oil",
        "Eggs", "Milk", "Buttermilk", "Heavy cream", "Sour cream", "Cream cheese",
        "Condensed milk", "Evaporated milk",
        "Vanilla extract", "Almond extract", "Honey", "Maple syrup",
        "Chocolate chips", "White chocolate", "Chopped nuts", "Sprinkles", 
        "Coconut flakes", "Dried fruit",
        "Lemon zest", "Lemon juice", "Bananas", "Applesauce"
    ]

    added = 0
    for name in common_ingredients:
        if not Ingredient.query.filter_by(name=name).first():
            db.session.add(Ingredient(name=name))
            added += 1
    db.session.commit()
    return f"✅ Populated {added} new ingredients!"



if __name__ == "__main__":
    app.run(debug=True)
