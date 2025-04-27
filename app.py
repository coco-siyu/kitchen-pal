from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# A simple storage for now (we'll upgrade to a database later!)
recipes = []

@app.route("/")
def home():
    return render_template("index.html", recipes=recipes)

@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        
        recipes.append({
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions
        })
        return redirect(url_for('home'))
    
    return render_template("add_recipe.html")

if __name__ == "__main__":
    app.run(debug=True)
