from flask import Flask, render_template
from models import Recipe

app = Flask(__name__)


shopping_list = []


recipe_ratings = {}


@app.route('/rate_recipe', methods=['POST'])
def rate_recipe():
    recipe_name = request.form['recipe_name']
    rating = int(request.form['rating'])
    if recipe_name not in recipe_ratings:
        recipe_ratings[recipe_name] = []
    recipe_ratings[recipe_name].append(rating)
    return redirect(url_for('recipe_details', recipe_name=recipe_name))


@app.route('/recipe_details/<recipe_name>')
def recipe_details(recipe_name):
    ratings = recipe_ratings.get(recipe_name, [])
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    return render_template('recipe_details.html', recipe_name=recipe_name, avg_rating=avg_rating, ratings=ratings)


@app.route('/add_to_shopping_list', methods=['POST'])
def add_to_shopping_list():
    item = request.form['item']
    shopping_list.append(item)
    return redirect(url_for('shopping_list'))


@app.route('/shopping_list')
def view_shopping_list():
    return render_template('shopping_list.html', shopping_list=shopping_list)


# Hardcoded list of recipes
recipes = [
    Recipe('Spaghetti', ['pasta', 'tomato sauce', 'cheese'],
           'Boil pasta, add sauce, top with cheese'),
    Recipe('Salad', ['lettuce', 'tomato', 'cucumber'],
           'Mix ingredients together')
]


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here you can implement logic to handle the message (e.g., send an email)
        flash(f"Message received from {name}!")
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '')
    if query:
        # Filter recipes based on query (this is a basic example)
        filtered_recipes = [recipe for recipe in
                            recipes if query.lower() in recipe['name'].lower()]
    else:
        filtered_recipes = recipes  # Return all if no query
    return render_template('search_results.html',
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


@app.route('/recipes')
def recipes():
    page = request.args.get('page', 1, type=int)
    recipes_per_page = 5
    start = (page - 1) * recipes_per_page
    end = start + recipes_per_page
    paginated_recipes = recipes[start:end]
    return render_template('recipes.html',
                           recipes=paginated_recipes, page=page)


@app.route('/recipe/<string:name>')
def recipe_detail(name):
    recipe = next((r for r in recipes if r.name == name), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    return "Recipe not found", 404


if __name__ == '__main__':
    app.run(debug=True)
