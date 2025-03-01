from flask import Flask, render_template
from models import Recipe

app = Flask(__name__)

# Hardcoded list of recipes
recipes = [
    Recipe('Spaghetti', ['pasta', 'tomato sauce', 'cheese'],
           'Boil pasta, add sauce, top with cheese'),
    Recipe('Salad', ['lettuce', 'tomato', 'cucumber'],
           'Mix ingredients together')
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/recipes')
def recipe_list():
    return render_template('recipes.html', recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)
