FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./
COPY ./unit_commitment/ ./unit_commitment/
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false  && \ 
    poetry install

EXPOSE 8888
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD uvicorn unit_commitment.app:app --reload --host 0.0.0.0 --port 8888