# Start from a small official Python image (same Python version CI uses)
FROM python:3.9-slim

# Set the working directory in the container.
# Every command below runs inside /app, and the code is copied here.
WORKDIR /app

# Install dependencies.
# requirements.txt is copied on its own first, so Docker can cache this
# layer: dependencies are only reinstalled when requirements.txt changes,
# not every time app.py changes. --no-cache-dir keeps the image smaller.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code:
# app.py, templates/ (form.html, result.html) and model/model.pkl
COPY . .

# Document the port Flask listens on (app.py: port=5000)
EXPOSE 5000

# Run the app. app.py starts Flask on 0.0.0.0:5000, so it is reachable
# from outside the container (127.0.0.1 would only work inside it).
CMD ["python", "app.py"]
