import re
import unittest
from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

	def setUp(self):
		app.testing = True
		self.client = app.test_client()

	def test_model_app_integration(self):
		# Valid test input that should work with the trained model
		form_data = {
			'temperature': '275.15',   # Kelvin
			'pressure': '1013',        # hPa
			'humidity': '85',          # %
			'wind_speed': '3.6',       # m/s
			'wind_deg': '180',         # degrees
			'rain_1h': '0',            # mm
			'rain_3h': '0',            # mm
			'snow': '0',               # mm
			'clouds': '20'             # %
		}

		response = self.client.post('/', data=form_data)
		self.assertEqual(response.status_code, 200)

		html_text = response.data.decode('utf-8').lower()

		# Ensure that the result page (response.data) includes a weather prediction
		self.assertIn('the weather is', html_text)

		# Ensure that the result page includes a prediction time
		self.assertIn('prediction time', html_text)
		self.assertRegex(html_text, r'prediction time:</strong>\s*[\d.]+\s*ms')

		valid_classes = [
			'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
			'misty', 'rainy', 'smokey', 'thunderstorm'
		]
		match = re.search(r'the weather is:</strong>\s*([a-z]+)', html_text)
		prediction = match.group(1) if match else None

		# Ensure that classification is in valid classes, provide an error message if not.
		self.assertIn(
			prediction, valid_classes,
			f"Prediction '{prediction}' is not one of the 9 valid weather classes"
		)

if __name__ == '__main__':
	unittest.main()
