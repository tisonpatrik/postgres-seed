# Using the specified Python version
FROM python:3.10

# Setting some environment variables to improve Python execution within Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Remove the PYTHONPATH environment variable setting since it might be causing issues
# ENV PYTHONPATH /home/app

# Setting the working directory in the container
WORKDIR /home/app

# Copying the poetry dependency files to the working directory
COPY docker-app/pyproject.toml docker-app/poetry.lock* ./

# Installing poetry and the project dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev

# Copying the source code to the working directory
COPY docker-app/src ./src

# Copying the shared directory into the container
COPY ../shared /home/app/shared

# Specifying the default command to run the FastAPI app with uvicorn
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
