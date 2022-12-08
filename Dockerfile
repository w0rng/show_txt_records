FROM python:3.11.0 as builder

WORKDIR /app

RUN pip install --upgrade pip pdm

COPY pyproject.toml pdm.lock ./
RUN mkdir __pypackages__ &&\
    pdm install --prod --no-lock --no-editable


FROM python:3.11.0-alpine3.17
WORKDIR /app

COPY --from=builder /app/__pypackages__/3.11 /pkgs
ENV PYTHONPATH="${PYTHONPATH}:/pkgs/lib" \
    PATH="${PATH}:/pkgs/bin"

COPY ./src /app/

CMD ["gunicorn", "main:app", "--worker-class", "aiohttp.GunicornWebWorker", "-c", "gunicorn.conf.py"]