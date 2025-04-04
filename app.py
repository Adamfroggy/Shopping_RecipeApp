from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES
from models import Recipe

app = Flask(__name__)


shopping_list = []


recipe_ratings = {}

# sample categories to the recipes
recipes = [
    {"name": "Pancakes", "category": "Breakfast"},
    {"name": "Spaghetti", "category": "Dinner"},
    {"name": "Chocolate Cake", "category": "Dessert"},
]


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form['name']
    category = request.form['category']
    recipes.append({"name": name, "category": category})
    return redirect(url_for('home'))


@app.route('/categories')
def categories():
    # Get unique categories
    categories = set([recipe['category'] for recipe in recipes])
    return render_template('categories.html', categories=categories)


@app.route('/rate_recipe', methods=['POST'])
def rate_recipe():
    recipe_name = request.form['recipe_name']
    rating = int(request.form['rating'])
    if recipe_name not in recipe_ratings:
        recipe_ratings[recipe_name] = []
    recipe_ratings[recipe_name].append(rating)
    return redirect(url_for('recipe_details', recipe_name=recipe_name))


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
