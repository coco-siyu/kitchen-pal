from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# config sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

 # automatically creates tables if not yet created
with app.app_context():
    db.create_all()
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=True)
    ingredient = db.relationship('Ingredient')
    instructions = db.Column(db.Text, nullable=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
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
        ingredient_id = request.form.get("ingredient_id")
        instructions = request.form["instructions"]
        new_recipe = Recipe(title=title, instructions=instructions, ingredient_id=ingredient_id)

        db.session.add(new_recipe)
        db.session.commit()
        # recipes.append({
        #     "title": title,
        #     "ingredients": ingredients,
        #     "instructions": instructions
        # })
        return redirect(url_for('home'))
    
    return render_template("add_recipe.html", ingredients = ingredients)

if __name__ == "__main__":
    app.run(debug=True)
