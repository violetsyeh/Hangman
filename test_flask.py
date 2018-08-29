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
				sess['num_guesses_remain'] = 4
				sess['correct_guesses'] = ''
				sess['incorrect_guesses'] = ''

	def test_session_check_incorrect_guess(self):
		"""Test session incorrect guess in "/check-guess" route."""

		result = self.client.get('/check-guess', query_string={"letter": 'q'}, follow_redirects=True)
		self.assertIsInstance(result.data, str)
		self.assertTrue('homepage.html')
		self.assertIn('{"answer":"incorrect","incorrect_guesses":"q ","num_guesses_remain":3,"updated_guess":"_ _ _ _"}\n', result.data)

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
				sess['num_guesses_remain'] = 4
				sess['correct_guesses'] = ''
				sess['incorrect_guesses'] = ''

	def test_session_check_incorrect_guess(self):
		"""Test session correct guess in "/check-guess" route."""

		result = self.client.get('/check-guess', query_string={"letter": 't'}, follow_redirects=True)
		self.assertIsInstance(result.data, str)
		self.assertTrue('homepage.html')
		self.assertIn('{"answer":"correct","num_guesses_remain":4,"updated_guess":"t_ _ t"}\n', result.data)


	# def test_check_game_status(self):
	# 	"""Test "/check-game-status" route."""

	# 	result = self.client.get('/check-game-status')
	# 	# self.assertIn('Play Again', result.data)
	# 	# self.assertTrue('homepage.html')




##############################################################################

if __name__ == "__main__":
	import unittest

	unittest.main()

