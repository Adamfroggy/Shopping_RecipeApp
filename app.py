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


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') if request.method == 'POST' else ''
    filtered_recipes = [recipe for recipe in recipes
                        if query.lower() in recipe.name.lower()]
    return render_template('search.html',
                           recipes=filtered_recipes, query=query)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate credentials (this is just a simple example)
        if username == 'admin' and password == 'password':
            # Replace with real validation
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, try again.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # This is just a placeholder for real session management
    return redirect(url_for('home'))


@app.route('/recipes')
def recipe_list():
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipe/<string:name>')
def recipe_detail(name):
    recipe = next((r for r in recipes if r.name == name), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    return "Recipe not found", 404


if __name__ == '__main__':
    app.run(debug=True)
