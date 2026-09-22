FROM python:3.12-slim

# Python should write directly to stdout/stderr
# and should not create .pyc files in the container.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip first.
RUN python -m pip install --upgrade pip

# Copy dependency metadata first so Docker can cache
# dependency installation separately from source-code changes.
COPY pyproject.toml README.md ./

# Copy source code required to build/install the project.
COPY src ./src

# Install the project and development dependencies.
RUN pip install --no-cache-dir ".[dev]"

# Copy runtime files used by the application and pipeline.
COPY database ./database
COPY scripts ./scripts
COPY data ./data

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]