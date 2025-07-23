from flask import Flask, render_template, jsonify, request, redirect, \
    url_for ,flash
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime
import random

app = Flask(__name__)


shopping_list = []


recipe_ratings = {}

# sample categories to the recipes


class Recipe:
    def __init__(self, name, ingredients, instructions, category=None,
                 prep_time=None):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category
        self.prep_time = prep_time


recipes = [
    Recipe('Spaghetti', ['pasta', 'tomato sauce', 'cheese'],
           'Boil pasta, add sauce, top with cheese', category='Dinner'),
    Recipe('Salad', ['lettuce', 'tomato', 'cucumber'],
           'Mix ingredients together', category='Lunch'),
    Recipe('Pancakes', ['Flour', 'Eggs', 'Milk'],
           'Mix ingredients and cook on a hot griddle.', category='Breakfast', 
           prep_time='10 mins'),
]


class Recipe:
    def __init__(self, name, ingredients, instructions, category=None, prep_time=None, last_updated=None):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category
        self.prep_time = prep_time
        self.last_updated = last_updated or "Unknown"


@app.route('/api/recipes')
def api_recipes():
    return jsonify(recipes)


@app.route('/add_recipe', methods=['GET'])
def add_recipe_form():
    return render_template('add_recipe.html')


@app.route('/recipe_details/<recipe_name>')
def recipe_details(recipe_name):
    recipe = next((r for r in recipes if r.name == recipe_name), None)
    if recipe:
        return render_template('recipe_details.html', recipe=recipe)
    else:
        return "Recipe not found", 404


@app.route('/update_recipe/<recipe_name>')
def update_recipe(recipe_name):
    recipe = next((r for r in recipes if r['name'] == recipe_name), None)
    if recipe:
        recipe['last_updated'] = datetime.now()
    return redirect(url_for('recipe_details', recipe_name=recipe_name))


@app.route('/filter_by_category/<category>')
def filter_by_category(category):
    filtered_recipes = [r for r in recipes if r['category'].lower() ==
                        category.lower()]
    return render_template('index.html', recipes=filtered_recipes)


@app.route('/sort')
def sort_recipes():
    sorted_recipes = sorted(recipes, key=lambda x: x['name'].lower())
    return render_template('index.html', recipes=sorted_recipes)


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


@app.route('/page/<int:page_num>')
def paginate_recipes(page_num):
    per_page = 5
    start = (page_num - 1) * per_page
    end = start + per_page
    paginated_recipes = recipes[start:end]
    return render_template('index.html', recipes=paginated_recipes,
                           page_num=page_num)


@app.route('/')
def home():
    selected_category = request.args.get('category', '')

    # Filter by category
    if selected_category:
        filtered = [r for r in recipes if r.get('category') 
                    == selected_category]
    else:
        filtered = recipes

    # Get categories from all recipes
    categories = list(set(r.get('category', 'Uncategorized') for r in recipes))

    # Counts
    breakfast_count = sum(1 for r in recipes if r.get('category') 
                          == 'Breakfast')
    dinner_count = sum(1 for r in recipes if r.get('category') == 'Dinner')

    # Recipe of the Day (from the full recipe list, not filtered)
    featured = random.choice(recipes) if recipes else None

    return render_template(
        'index.html',
        recipes=filtered,
        featured=featured,
        breakfast_count=breakfast_count,
        dinner_count=dinner_count,
        recipe_count=len(recipes),
        categories=categories,
        selected_category=selected_category
    )


@app.route('/categories')
def categories():
    categories = list(set(r.get('category', 'Uncategorized') for r in recipes))
    return render_template('categories.html', categories=categories)


@app.route('/rate_recipe/<recipe_name>/<float:rating>')
def rate_recipe(recipe_name, rating):
    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.')
        return redirect(url_for('recipe_details', recipe_name=recipe_name))
    recipe = next((r for r in recipes if r['name'] == recipe_name), None)
    if recipe:
        recipe['rating'] = rating
        flash(f'You rated {recipe_name} {rating} stars!')
    else:
        flash('Recipe not found.')
    return redirect(url_for('recipe_details', recipe_name=recipe_name))


@app.route('/clear_favorites')
def clear_favorites():
    favorite_recipes.clear()
    return redirect(url_for('home'))


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form['name']
    category = request.form['category']
    recipes.append({"name": name, "category": category})
    return redirect(url_for('home'))


photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
configure_uploads(app, photos)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        flash('Image uploaded successfully!')
        return redirect(url_for('home'))
    return 'No file uploaded', 400


@app.route('/sort_recipes/<sort_by>')
def sort_recipes(sort_by):
    if sort_by == "name":
        sorted_recipes = sorted(recipes, key=lambda x: x['name'])
    elif sort_by == "category":
        sorted_recipes = sorted(recipes, key=lambda x: x['category'])
    else:
        sorted_recipes = recipes
    return render_template('index.html', recipes=sorted_recipes)


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
    total_recipes = len(recipes)
    return render_template('index.html', total_recipes=total_recipes,
                           recipes=recipes)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    filtered_recipes = [r for r in recipes if query in r['name'].lower()]
    return render_template('search_results.html', recipes=filtered_recipes,
                           query=query)


@app.route('/remove_recipe/<recipe_name>')
def remove_recipe(recipe_name):
    global recipes
    recipes = [r for r in recipes if r['name'] != recipe_name]
    return redirect(url_for('home'))


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/recipe/<string:name>')
def recipe_detail(name):
    recipe = next((r for r in recipes if r.name == name), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    return "Recipe not found", 404


if __name__ == '__main__':
    app.run(debug=True)
