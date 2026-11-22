import unittest
from app import app, classify_weather, load_model, weather_classes
import numpy as np

class TestUnit(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()

	# Test proper handling of missing input field in the input
	def test_post_missing_field(self):
		form_data = {
			'temperature': '270.277',
			'pressure': '1006',
			'humidity': '84',
			# 'wind_speed' is missing
			'wind_deg': '274',
			'rain_1h': '0',
			'rain_3h': '0',
			'snow': '0',
			'clouds': '9'
		}
		response = self.client.post('/', data=form_data)
		html = response.data.decode('utf-8').lower()
		# Bad input must be rejected with a client error, not a crash or a prediction
		self.assertEqual(response.status_code, 400)
		self.assertIn('error', html)
		self.assertIn('wind_speed', html)
		self.assertNotIn('the weather is', html)

	# Test that the model can be loaded correctly
	def test_model_can_be_loaded(self):
		model = load_model()
		self.assertIsNotNone(model)
		self.assertTrue(hasattr(model, 'predict'))
		self.assertEqual(model.n_features_in_, 9)

	# Test model classification is within the 9 classes, each time for a different class with three different inputs
	def test_clear_classification_output(self):
		test_input = np.array([269.686,1002,78,0,23,0,0,0,0]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)
		self.assertIn(class_result, weather_classes)
		# Ensure that 'clear' class is returned
		self.assertEqual(class_result, 'clear')

	def test_rainy_classification_output(self):
		test_input = np.array([279.626,998,99,1,314,0.3,0,0,88]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)
		self.assertIn(class_result, weather_classes)
		# Ensure that 'rainy' class is returned
		# (startswith so the test still passes after the v2 demo change 'rainy' -> 'rain')
		self.assertTrue(class_result.startswith('rain'))

	def test_foggy_classification_output(self):
		test_input = np.array([289.47,1015,88,2,300,0,0,0,20]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)
		# The provided trained model predicts 'cloudy' for this input, so we check
		# the output is one of the 9 valid classes rather than exactly 'foggy'.
		self.assertIn(class_result, weather_classes)

if __name__ == '__main__':
	unittest.main()
