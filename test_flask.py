from unittest import TestCase
from model import connect_to_db, db, Score
from server import app
import server
from flask import session


class FlaskTestsBasic(TestCase):
	"""Flask tests."""

	def setUp(self):
		"""Set up to be done before every test."""

		#Get the Flask test client.
		self.client = app.test_client()

		#Show Flask errors during test.
		app.config['TESTING'] = True

	def test_index(self):
		"""Test homepage."""

		result = self.client.get("/")
		self.assertIn('Guessing Word Game', result.data)
		self.assertEqual(result.status_code, 200)
		self.assertIn('Guess the Secret Word', result.data)
		self.assertTrue('homepage.html')
		self.assertIn('You have ', result.data)
		self.assertIn(' guesses left', result.data)


class FlaskRouteTests(TestCase):
	"""Flask testing for routes."""

	def setUp(self):
		"""Set up to be done before every test."""

		#Get the Flask test client.
		self.client = app.test_client()

		#Show Flask errors during test.
		app.config['TESTING'] = True

	def test_get_secret_word(self):
		"""Test "/get-secret-word" route."""

		result = self.client.get('/get-secret-word')
		self.assertIn('_ ', result.data)
		self.assertEqual(result.status_code, 200)
		self.assertTrue('homepage.html')


class FlaskSessionIncorrectGuessTest(TestCase):
	"""Flask tests with user logged in to session."""

	def setUp(self):
		"""Set up to be done before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = "ABC"
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				"""Assign session values."""
				sess['secret_word'] = 'test'
				sess['updated_guess'] = '_ _ _ _'
				sess['num_guesses_remain'] = 6
				sess['correct_guesses'] = ''
				sess['incorrect_guesses'] = ''

	def test_session_check_incorrect_guess(self):
		"""Test session incorrect guess in "/check-guess" route."""

		result = self.client.get('/check-guess', query_string={"letter": 'q'}, follow_redirects=True)
		self.assertIsInstance(result.data, str)
		self.assertTrue('homepage.html')
		self.assertIn('{"answer":"incorrect","incorrect_guesses":"q ","num_guesses_remain":5,"updated_guess":"_ _ _ _"}\n', result.data)

class FlaskSessionCorrectGuessTest(TestCase):
	
	def setUp(self):
		"""Set up to be done before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = "ABC"
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				"""Assign session values."""
				sess['secret_word'] = 'test'
				sess['updated_guess'] = '_ _ _ _'
				sess['num_guesses_remain'] = 6
				sess['correct_guesses'] = ''
				sess['incorrect_guesses'] = ''

	def test_session_check_correct_guess(self):
		"""Test session correct guess in "/check-guess" route."""

		result = self.client.get('/check-guess', query_string={"letter": 't'}, follow_redirects=True)
		self.assertIsInstance(result.data, str)
		self.assertTrue('homepage.html')
		self.assertIn('{"answer":"correct","num_guesses_remain":6,"updated_guess":"t_ _ t"}\n', result.data)

class FlaskSessionWonGameTest(TestCase):

	def setUp(self):
		"""Set up to be done before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = "ABC"
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				"""Assign session values."""
				sess['secret_word'] = 'test'
				sess['updated_guess'] = 't _ s t'
				sess['num_guesses_remain'] = 3
				sess['correct_guesses'] = 'ts'
				sess['incorrect_guesses'] = 'q w a'

	def test_session_check_win_game(self):
		"""Test "/check-game-status" winning."""

		result = self.client.get('/check-guess', query_string={"letter": "e"}, follow_redirects=True)
		self.assertIn('{"game_status":"game won","updated_guess":"test"}\n', result.data)
		self.assertTrue('homepage.html')

class FlaskSessionLostGameTest(TestCase):

	def setUp(self):
		"""Set up to be done before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = "ABC"
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				"""Assign session values."""
				sess['secret_word'] = 'test'
				sess['updated_guess'] = '_ e _ _'
				sess['num_guesses_remain'] = 1
				sess['correct_guesses'] = 'e'
				sess['incorrect_guesses'] = 'q w a z k'

	def test_session_check_lost_game(self):
		"""Test "/check-game-status" winning."""

		result = self.client.get('/check-guess', query_string={"letter": "y"}, follow_redirects=True)
		self.assertIn('{"game_status":"game lost","updated_guess":"_ e _ _"}\n', result.data)
		self.assertTrue('homepage.html')

class FlaskSessionRepeatGuess(TestCase):

	def setUp(self):
		"""Set up to be done before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = "ABC"
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				"""Assign session values."""
				sess['secret_word'] = 'test'
				sess['updated_guess'] = 't _ _ t'
				sess['num_guesses_remain'] = 5
				sess['correct_guesses'] = 't'
				sess['incorrect_guesses'] = 'z'

	def test_session_repeat_guess(self):
		"""Test helper function check_repeat_letter."""

		result = self.client.get('/check-guess', query_string={"letter": "z"}, follow_redirects=True)
		self.assertIn('{"guess":"tried already"}\n', result.data)
		self.assertTrue('homepage.html')

##############################################################################

if __name__ == "__main__":
	import unittest

	unittest.main()

