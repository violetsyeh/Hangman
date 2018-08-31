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
WORDS_URL = 'http://app.linkedin-reach.io/words'


@app.route("/")
def index():
    """Homepage."""
    session.clear()
    return render_template('homepage.html')


@app.route("/get-secret-word", methods=['GET'])
def display_secret_word():
    """Display secret word user will guess."""

    # difficulty = request.form.get('difficulty')
    # payload = {'difficulty': random.randint(1, 3)}
    # payload = {'difficulty': 1}
    # words = requests.get(url=WORDS_URL, params=payload)
    # words = str(words.text)
    # words = words.split()
    # secret_word = random.choice(words)
    secret_word = generate_secret_word(None)

    session['secret_word'] = secret_word
    session['updated_guess'] = len(secret_word) * '_ '
    session['num_guesses_remain'] = MAX_GUESSES
    session['correct_guesses'] = ''
    session['incorrect_guesses'] = ''
    session['incorrect_whole_words'] = ''

    print secret_word
    return len(secret_word) * '_ '

@app.route("/change-difficulty", methods=['GET'])
def change_difficulty():
    """Change difficulty based on number user entered, 1-10."""

    difficulty = int(request.args.get("difficulty"))
    print difficulty
    secret_word = generate_secret_word(difficulty)
    print secret_word

    return len(secret_word) * '_ '
    


@app.route("/check-guess", methods=['GET'])
def check_guess():
    """Check letter guess if in secret word."""

    updated_guess = session['updated_guess']
    secret_word = session['secret_word']
    num_guess = session['num_guesses_remain']
    updated_guess = ''
    result = {}
    guess_status = 'incorrect guess'

    while num_guess >= MAX_ERRORS_COUNTER:

        letter = request.args.get("letter").lower()
        print letter

        
        if check_repeat_letter(letter):

            for i in range(len(secret_word)):

                if secret_word[i] == letter:
                    updated_guess = updated_guess + letter
                    guess_status = 'correct guess'

                elif secret_word[i] in session['correct_guesses']:
                    updated_guess = updated_guess + secret_word[i]

                else:
                    updated_guess = updated_guess + '_ '

                session['updated_guess'] = updated_guess
                session['correct_guesses'] = session['correct_guesses'] + letter
            
            if guess_status == 'correct guess':    
                result['updated_guess'] = session['updated_guess']
                result['answer'] = 'correct'
                result['num_guesses_remain'] = num_guess

                if secret_word == session['updated_guess']:
                    return redirect('/check-game-status')
                return jsonify(result)

            if guess_status == 'incorrect guess':
                session['num_guesses_remain'] -= 1
                session['incorrect_guesses'] = session['incorrect_guesses'] + letter + ' '

                result['updated_guess'] = session['updated_guess']
                result['answer'] = 'incorrect'
                result['num_guesses_remain'] = session['num_guesses_remain']
                result['incorrect_guesses'] = session['incorrect_guesses']  + session['incorrect_whole_words']

                if session['num_guesses_remain'] == MAX_ERRORS_COUNTER:
                    return redirect('/check-game-status') 

                return jsonify(result)                
        else:
            result['guess'] = 'tried already'
            return jsonify(result)

        return redirect('/check-game-status')

@app.route('/check-whole-word')
def check_whole_word():
    """Check if whole word user entered matches secret word."""

    results = {}
    word = request.args.get("word").lower()
    print word

    if session['secret_word'] == word:
        results['game_status'] = 'game won'
        results['updated_guess'] = session['secret_word']
        return jsonify(results)


    else:
        session['num_guesses_remain'] -= 1
        session['incorrect_whole_words'] = session['incorrect_whole_words'] + word + ' '

        results['updated_guess'] = session['updated_guess']
        results['whole_word_guess'] = 'incorrect'
        results['num_guesses_remain'] = session['num_guesses_remain']
        results['incorrect_guesses'] = session['incorrect_guesses'] + session['incorrect_whole_words']

        if session['num_guesses_remain'] == 0:
            return redirect('check-game-status')
        return jsonify(results)



@app.route('/check-game-status')
def check_game_status():
    """Return status of game, won or lost."""

    results = {}

    if session['num_guesses_remain'] == MAX_ERRORS_COUNTER:
        results['game_status'] = 'game lost'
        results['updated_guess'] = session['updated_guess']
        return jsonify(results)

    elif session['secret_word'] == session['updated_guess']:
        results['game_status'] = 'game won'
        results['updated_guess'] = session['updated_guess']
        return jsonify(results)
        
    





####################################################################################
#Helper functions

def check_repeat_letter(letter):
    """Check if letter entered has already been submitted before."""
    ######################################
    #####################################
    ####################################
    ### make it return true because it is checking if there is a repeat letter 
    if letter in session['correct_guesses']:
        return False
    elif letter in session['incorrect_guesses']:
        return False 
    else:
        return True

def generate_secret_word(difficulty):
    """Generate secret word from API."""

    if difficulty: 
        payload = {'difficulty': difficulty}
        words = requests.get(url=WORDS_URL, params=payload)
        words = str(words.text)
        words = words.split()
        secret_word = random.choice(words)
        return secret_word
    else:
        payload = {'difficulty': random.randint(1, 3)}
        words = requests.get(url=WORDS_URL, params=payload)
        words = str(words.text)
        words = words.split()
        secret_word = random.choice(words)

        return secret_word


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
