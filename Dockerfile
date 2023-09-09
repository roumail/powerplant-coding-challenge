FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    # poetry config virtualenvs.create false  && \ 
    poetry install --no-dev

EXPOSE 8888
CMD ["poetry", "run", "production-plan-api"]
# ENTRYPOINT [ ]