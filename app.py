from os.path import splitext
from uuid import uuid4
from datetime import datetime
from base64 import b64encode
from flask import Flask, render_template, request
from textwrap import indent
from re import compile, sub

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}


def allowed_file(filename):
    if filename:
        file_ext = splitext(filename)[1]
        return file_ext.lower() in ALLOWED_EXTENSIONS
    return False


def filename(id,type='yml'):
    # return f'cookbook/{id}.{type}'
    return f'cookbook/{datetime.now():%Y%m%dT%H%M%S}.{type}'


def number_lines(data):
    directions = compile('\n+').split(data)
    numbered = []
    count = 1
    for line in directions:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('#'):
            count = 1
            numbered.append('')
            numbered.append(line)
            continue

        numbered.append(("{0}. {1}".format(count, line)))
        count = count + 1

    return '\n'.join(numbered)


def replace_fractions(v):
    '''
    https://bit.ly/2XB3nBA
    1 4 1/2-pound whole chicken, patted dry
    1/2 teaspoon freshly ground black pepper
    1-1/2 cloves garlic
    About 1/2 teaspoon salt
    '''
    val = str(v)

    val = sub(r'(?<=\D\s)1\/8|(?<=\d)[\s-]1\/8', '⅛', val)
    val = sub(r'(?<=\D\s)1\/4|(?<=\d)[\s-]1\/4', '¼', val)
    val = sub(r'(?<=\D\s)1\/3|(?<=\d)[\s-]1\/3', '⅓', val)
    val = sub(r'(?<=\D\s)1\/2|(?<=\d)[\s-]1\/2', '½', val)
    val = sub(r'(?<=\D\s)2\/3|(?<=\d)[\s-]2\/3', '⅔', val)
    val = sub(r'(?<=\D\s)5\/8|(?<=\d)[\s-]5\/8', '⅝', val)
    val = sub(r'(?<=\D\s)3\/4|(?<=\d)[\s-]3\/4', '¾', val)

    return val


@app.route('/')
def index():
    return render_template('input.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name', None)
        servings = request.form.get('servings', None)
        source = request.form.get('source', None)
        source_url = request.form.get('source_url', None)
        prep_time = request.form.get('prep_time', None)
        cook_time = request.form.get('cook_time', None)
        categories = request.form.get('categories', None)
        notes = request.form.get('notes', None)
        description = request.form.get('description', None)
        ingredients = request.form.get('ingredients', None)
        directions = request.form.get('directions', None)
        recipe_photo = request.files.get('recipe_photo', None)

        id = uuid4()
        doc = f'id: {id}\n'
        if recipe_name:
            recipe_name = recipe_name.strip()
            doc = doc + f'name: {recipe_name.title()}\n'
        if servings:
            servings = servings.strip()
            doc = doc + f'servings: {servings}\n'
        if source:
            source = source.strip()
            doc = doc + f'source: {source}\n'
        if source_url:
            source_url = source_url.strip()
            doc = doc + f'source_url: {source_url}\n'
        if prep_time:
            prep_time = prep_time.strip()
            doc = doc + f'prep_time: {prep_time}\n'
        if cook_time:
            cook_time = cook_time.strip()
            doc = doc + f'cook_time: {cook_time}\n'
        if categories:
            cats = ''.join(categories.split())
            cats = ', '.join([i.strip() for i in cats.split(',')])
            doc = doc + f'categories: [{cats}]\n'
        if notes:
            notes = sub('\n\s+\n', '\n', notes)
            notes = notes.strip()
            notes = replace_fractions(notes)
            doc = doc + 'notes: |\n'
            doc = doc + indent(notes, '  ')
            doc = doc + '\n'
        if description:
            description = sub('\n\s+\n', '\n', description)
            description = description.strip()
            description = replace_fractions(description)
            doc = doc + 'description: |\n'
            doc = doc + indent(description, '  ')
            doc = doc + '\n'
        if ingredients:
            ingredients = sub('\n\s+\n', '\n', ingredients)
            ingredients = '\n'.join([i.strip() for i in ingredients.split('\n')])
            ingredients = replace_fractions(ingredients)
            doc = doc + 'ingredients: |\n'
            doc = doc + indent(ingredients, '  ')
            doc = doc + '\n'
        if directions:
            directions = sub('\n\s+\n', '\n', directions)
            directions = '\n'.join([i.strip() for i in directions.split('\n')])
            directions = replace_fractions(directions)
            directions = number_lines(directions)
            directions = directions.strip()
            doc = doc + 'directions: |\n'
            doc = doc + indent(directions, '  ')
            doc = doc + '\n'
        if recipe_photo and allowed_file(recipe_photo.filename):
            photo_data = b64encode(recipe_photo.read()).decode("utf-8") 
            doc = doc + f'photo: {photo_data}'

        with open(filename(id), 'w') as f:
            f.write(doc)

    return render_template('result.html', status='ok')
