# Hangman

Implemented a game of Hangman, where the user plays "against" the computer. The secret-keeper (the computer) thinks of a word and the guesser (the user) tries to guess it one letter at a time. If the guesser is feeling confident, they can try solve the entire word. The guesser has six lives (incorrect guesses) and if the word is not completely solved, game over. If the guesser guesses a letter that is part of the word, all occurrences of that letter is revealed. If all letters are revealed through guessing, they have won. The user may also choose a difficulty level between 1 and 10, otherwise, a secret-word will be chosen at random. 

## Contents
* [Tech Stack](#technologies)
* [Game Play](#gameplay)
* [Installation](#install)
* [Version 2.0](#version)
* [About Me](#aboutme)

## <a name="technologies"></a>Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Bootstrap, HTML5, CSS3<br/>
APIs: LinkedIn Reach Words<br/>

## <a name="features"></a>Features
![gameplay](/static/images/readme/Hangman.gif)</br>


## <a name="install"></a>Installation

To run Hangman:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/violetsyeh/Hangman
```

Create and activate a virtual environment inside your Hangman directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access Hangman.

## <a name="version"></a>Version 2.0
* Leaderboard to display top scores
* Cache API results to only make one API request
* Cache secret words the user has already solved before

## <a name="aboutme"></a>About Me
Violet Yeh is a Software Engineer in the Bay Area.
Learn more about Violet on [LinkedIn](http://www.linkedin.com/in/violetsyeh).