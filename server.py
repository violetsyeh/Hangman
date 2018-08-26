"""Word Guessing Game Server."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Score
import requests
import random
ADJECTIVES = [
        'Juicy',
        'Delicious',
        'Aromatic',
        'Ripe',
        'Flavorful',
        'Reasonably-Priced',
        'Artisanally Hand-Crafted',
]

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def index():
    """Homepage."""
    return render_template('homepage.html')


# @app.route("/adjective")
# def get_random_adjective():
#     """Return a simple adjective."""

#     return generate_secret_word()


@app.route("/get_secret_word")
def generate_secret_word():

    # difficulty = request.form.get('difficulty')
    url = 'http://app.linkedin-reach.io/words'
    payload = {'difficulty': random.randint(1, 3)}
    words = requests.get(url=url, params=payload)
    words = str(words.text)
    words = words.split()
    secret_word = random.choice(words)
    return len(secret_word) * '_ '



####################################################################################
# Helper Functions

# def generate_secret_word():

#     url = 'http://app.linkedin-reach.io/words'
#     payload = {'difficulty': random.randint(1, 3)}
#     words = requests.get(url=url, params=payload)
#     words = str(words.text)
#     words = words.split()
#     secret_word = random.choice(words)
#     return secret_word


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
