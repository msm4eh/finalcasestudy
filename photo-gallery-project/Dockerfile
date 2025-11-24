FROM python:3.10-slim

WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

EXPOSE 5000

# run the app
CMD ["python", "src/app.py"]

