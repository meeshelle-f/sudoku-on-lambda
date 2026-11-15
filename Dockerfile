# Small official Python 3.13 image to build on
FROM python:3.13-slim

# AWS Lambda Web Adapter: passes Lambda requests to the web server.
# Outside Lambda it does nothing, so the same image runs with docker run.
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

# Work in /app inside the image
WORKDIR /app

# Install Flask and gunicorn first, so this layer is reused when only the code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the game
COPY app.py sudoku.py ./
COPY templates/ templates/

# Version shown in the page footer; the port and health check the adapter uses
ENV APP_VERSION="1.0" AWS_LWA_PORT=8080 AWS_LWA_READINESS_CHECK_PATH=/health

# Lambda does not run as root, so use port 8080 instead of 80
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
