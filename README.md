# KitchenPal 🍪

**KitchenPal** is a cozy, beginner-friendly web app to help you:
- Manage your favorite recipes
- Store ingredients
- Organize your personal kitchen inventory

Built with **Flask**, **SQLite**, and a warm baking vibe!

---

## ✨ Features

- Add and view recipes
- Select main ingredients from a dropdown (with preloaded pantry basics)
- Store recipe instructions
- Stylish card layout with cozy milk yellow theme
- Hover animations for a lively user experience
- Seed scripts to preload ingredients and recipes

---

## 📚 Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite (local database)
- HTML + CSS (Flexbox layout)
- Render (for deployment)

---

## 🛠 Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/kitchen-pal.git
   cd kitchen-pal


2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Install Dependencies:
    ```bash
    pip install -r requirements.txt

4. Create the db (this will create recipes.db):
    ```bash
    python app.py

5. Seed initial ingredients and recipes:
    ```bash
    python scripts/seed_ingredients.py
    python scripts/seed_recipes.py
This will generate some ingredients and recipes to prefill the web page

6. Run the app locally:
    ```bash
    python app.py
Visit http://127.0.0.1:5000/ to view your KitchenPal!

## 💌 Acknowledgments
Built with love for baking, organizing, and learning web development.
Enjoy managing your kitchen like a pro! 🧁✨
