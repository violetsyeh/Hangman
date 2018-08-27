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

	def test_check_word(self):
		"""Test "/check-word" route."""

		result = self.client.get('/check-word')
		self.assertIsInstance(result.data, str)
		self.assertTrue('homepage.html')

class FlaskSessionTest(TestCase):
	"""Flask tests with user logged in to session."""

	def setUp(self):

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = "ABC"
		self.client = app.test_client()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['secret_word'] = 'cat'
				sess['guess_word'] = '_ _ _'
				sess['num_guess'] = 1

	def test_session_check_word(self):
		"""Test session in "/check-word" route."""

		result = self.client.get('/check-word')
		self.assertIsInstance(result.data, str)







##############################################################################

if __name__ == "__main__":
	import unittest

	unittest.main()

