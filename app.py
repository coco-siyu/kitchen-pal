import os
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
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

# home page
@app.route("/")
def home():
    recipes = Recipe.query.all() # display everything
    return render_template("index.html", recipes=recipes)

# add recipe page
@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    # query alphabatically
    ingredients = Ingredient.query.order_by(Ingredient.name.asc()).all()
    
    if request.method == "POST":
        title = request.form["title"]
        ingredient_ids = request.form.getlist("ingredient_ids")
        instructions = request.form["instructions"]
        new_recipe = Recipe(title=title, instructions=instructions)

        # Add multiple selected ingredients
        selected_ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
        new_recipe.ingredients.extend(selected_ingredients)
        
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
    ingredient_ids = request.form.getlist("ingredient_ids")

    recipe.ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
    
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
    
    ingredients = Ingredient.query.all()
    return render_template("add_ingredient.html", ingredients=ingredients)

if __name__ == "__main__":
    app.run(debug=True)
