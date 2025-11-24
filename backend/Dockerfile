FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src

# Change working directory so Python can import sim_device_control
WORKDIR /app/src

EXPOSE 8000

CMD ["uvicorn", "sim_device_control.app:app", "--host", "0.0.0.0", "--port", "8000"]

