from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
import time

app = Flask(__name__)

weather_classes = ['clear', 'cloudy', 'drizzly', 'foggy', 'hazey', 'misty', 'rainy', 'smokey', 'thunderstorm']

def load_model(model_path='model/model.pkl'):
    # FIX 3: use "with" so the file is closed after loading
    with open(model_path, 'rb') as f:
        return pickle.load(f)

# FIX 3: load the model ONCE when the app starts, not on every request
model = load_model()

def classify_weather(features):
    # FIX 4: give the model its column names, as it was trained on a pandas DataFrame.
    # Without this, scikit-learn prints a "does not have valid feature names" warning on every prediction.
    features = pd.DataFrame(features, columns=model.feature_names_in_)
    start = time.time()
    prediction_index = model.predict(features)[0]
    latency = round((time.time() - start) * 1000, 2)
    # FIX 1: use the model's prediction instead of always returning weather_classes[1] ('cloudy')
    prediction = weather_classes[int(prediction_index)]

    return prediction, latency


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # FIX 2: convert the required fields to float (they arrive from the form as text)
            temperature = float(request.form['temperature'])
            pressure = float(request.form['pressure'])
            humidity = float(request.form['humidity'])
            wind_speed = float(request.form['wind_speed'])
            wind_deg = float(request.form['wind_deg'])
            rain_1h = float(request.form.get('rain_1h', 0) or 0)
            rain_3h = float(request.form.get('rain_3h', 0) or 0)
            snow = float(request.form.get('snow', 0) or 0)
            clouds = float(request.form.get('clouds', 0) or 0)

            features = np.array([
                temperature, pressure, humidity,
                wind_speed, wind_deg, rain_1h,
                rain_3h, snow, clouds
            ]).reshape(1, -1)

            prediction, latency = classify_weather(features)

            return render_template('result.html', prediction=prediction, latency=latency)

        except KeyError as e:
            error_msg = f"Error processing input: missing field {e}"
            return render_template('form.html', error=error_msg), 400
        except ValueError as e:
            error_msg = f"Error processing input: invalid value ({e})"
            return render_template('form.html', error=error_msg), 400
        except Exception as e:
            error_msg = f"Error processing input: {e}"
            return render_template('form.html', error=error_msg), 500
    # GET method: show the input form
    return render_template('form.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
