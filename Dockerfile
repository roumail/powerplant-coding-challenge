FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false 

# Build the package
RUN poetry build

# Install the package using pip
RUN pip install dist/*.whl

COPY ./app/ ./

ENV PYTHONPATH "${PYTHONPATH}:/app"


EXPOSE 8888
CMD uvicorn main:app --host 0.0.0.0 --port 8888
