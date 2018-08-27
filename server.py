"""Word Guessing Game Server."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Score
import requests
import random

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


@app.route("/get-secret-word")
def generate_secret_word():

    # difficulty = request.form.get('difficulty')
    url = 'http://app.linkedin-reach.io/words'
    payload = {'difficulty': random.randint(1, 3)}
    words = requests.get(url=url, params=payload)
    words = str(words.text)
    words = words.split()
    secret_word = random.choice(words)
    session['secret_word'] = secret_word
    session['word_guess'] = len(secret_word) * '_ '
    session['num_guess'] = 0
    session['correct_guesses'] = []
    print secret_word
    return len(secret_word) * '_ '

@app.route("/check-guess")
def check_guess():

    word_guess = session['word_guess']
    secret_word = session['secret_word']
    num_guess = session['num_guess']
    result = ''

    while num_guess < 7:

        letter = request.args.get("letter").lower()
        

        if letter in secret_word:
            for i in range(len(secret_word)):
                if secret_word[i] == letter:
                    result = result + letter
                elif secret_word[i] in session['correct_guesses']:
                    result = result + secret_word[i]
                else:
                    result = result + '_ '
            session['num_guess'] += 1
            # print session['num_guess']
            session['word_guess'] = result
            session['correct_guesses'].append(letter)
            print session['correct_guesses']
            return result
        else:
            flash('That letter is not in the secret word')
            session['num_guess'] += 1
            # print session['num_guess']
            session['word_guess'] = result
            session['incorrect_guesses'].append(letter)
            return result





####################################################################################



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
