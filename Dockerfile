# Stage 1: Build stage
FROM python:3.10-slim AS build
WORKDIR /app

# Copy dependencies and install them for local user
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Stage 2: Runtime stage
FROM python:3.10-slim AS runtime
WORKDIR /app

# Copy installed packages from build stage
COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy app code
COPY --from=build /app /app

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
