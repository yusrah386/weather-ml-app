import unittest
from app import app

class TestAppSmoke(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()

	# Test a success in running the application
	def test_prediction_route_success(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	# Test a form is rendered
	def test_get_form(self):
		response = self.client.get('/')
		html = response.data.decode('utf-8')
		self.assertIn('<form', html)
		self.assertIn('name="temperature"', html)
		self.assertIn('name="humidity"', html)
		self.assertIn('Predict', html)

if __name__ == '__main__':
	unittest.main()
