"""Word Guessing Game Server."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
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

MAX_ERRORS_COUNTER = 0
MAX_GUESSES = 6

@app.route("/")
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route("/get-secret-word")
def generate_secret_word():

    # difficulty = request.form.get('difficulty')
    url = 'http://app.linkedin-reach.io/words'
    # payload = {'difficulty': random.randint(1, 3)}
    payload = {'difficulty': 1}
    words = requests.get(url=url, params=payload)
    words = str(words.text)
    words = words.split()
    secret_word = random.choice(words)

    session['secret_word'] = secret_word
    session['updated_guess'] = len(secret_word) * '_ '
    session['num_guesses_remain'] = MAX_GUESSES
    session['correct_guesses'] = []
    session['incorrect_guesses'] = ''

    print secret_word
    return len(secret_word) * '_ '

@app.route("/check-guess")
def check_guess():

    updated_guess = session['updated_guess']
    secret_word = session['secret_word']
    num_guess = session['num_guesses_remain']
    updated_guess = ''
    result = {}

    while num_guess >= MAX_ERRORS_COUNTER:

        letter = request.args.get("letter").lower()
        

        if letter in secret_word:
            for i in range(len(secret_word)):
                if secret_word[i] == letter:
                    updated_guess = updated_guess + letter
                elif secret_word[i] in session['correct_guesses']:
                    updated_guess = updated_guess + secret_word[i]
                else:
                    updated_guess = updated_guess + '_ '
            session['updated_guess'] = updated_guess
            session['correct_guesses'].append(letter)
            

            if secret_word == session['updated_guess']:
                return redirect('/check-game-status')
            else:
                result['updated_guess'] = session['updated_guess']
                result['answer'] = 'correct'
                result['num_guesses_remain'] = num_guess
                return jsonify(result)
        else:
            session['num_guesses_remain'] -= 1
            session['incorrect_guesses'] = session['incorrect_guesses'] + letter + ' '

            if session['num_guesses_remain'] == MAX_ERRORS_COUNTER:
                return redirect('/check-game-status')
            else: 
                result['updated_guess'] = session['updated_guess']
                result['answer'] = 'incorrect'
                result['num_guesses_remain'] = session['num_guesses_remain']
                result['incorrect_guesses'] = session['incorrect_guesses']
                
            return jsonify(result)
    return redirect('/check-game-status')


@app.route('/check-game-status')
def check_game_status():

    result = {}

    if session['num_guesses_remain'] == MAX_ERRORS_COUNTER:
        result['game-status'] = 'game lost'
        result['updated_guess'] = session['updated_guess']
        return jsonify(result)
    elif session['secret_word'] == session['updated_guess']:
        result['game-status'] = 'game won'
        result['updated_guess'] = session['updated_guess']
        return jsonify(result)
        
    





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
