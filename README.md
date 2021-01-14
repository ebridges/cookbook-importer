# Cookbook Importer

Provides a simple UI for entering a recipe and formatting it into a format acceptable to import into [Paprika Recipe Manager](https://www.paprikaapp.com).

## Usage

### Saving a Recipe

To open the UI for entering a single recipe:

```sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ export FLASK_DEBUG=0
$ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

- this writes the recipe to a subfolder named `./cookbook`

### Combining for Import

To aggregate all recipes into a single file for importing into Paprika, run `aggregate.py`.

## Features

* Numbers the steps under directions.
* Converts fractional amounts to vulgar fractions (e.g. 1/4 -> ¼).
* Cleans out any extraneous whitespace in all fields.

## Example Output Format

Documented here: https://www.paprikaapp.com/help/mac/#importrecipes

_Note: not all fields are actually presented in the UI but can be easily added._

```yaml
name: My Tasty Recipe
servings: 4-6 servings
source: Food Network
source_url: http://www.google.com
prep_time: 10 min
cook_time: 30 min
on_favorites: yes
categories: [Dinner, Holiday]
nutritional_info: 500 calories
difficulty: Easy
rating: 5
notes: |
  This is delicious!!!
description: |
  This is my tasty recipe, it's delicious!!!
ingredients: |
  1/2 lb meat
  1/2 lb vegetables
  salt
  pepper
  2 tbsp olive oil
  4 cups flour
directions: |
  Mix things together.
  Eat.
  Tasty.
  Yum yum yum.
photo: (base-64 encoded image)
```

## License

MIT
