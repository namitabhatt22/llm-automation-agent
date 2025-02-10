FROM python:3.9

WORKDIR /app

# Copy source code and dependencies
COPY src/ /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 8000

# Run the application
ENTRYPOINT ["python3"]
CMD ["main.py"]
