# STAGE 1
FROM python:3.9.12-alpine3.15 AS compile-time

# Install compilation dependencies
RUN apk add gcc musl-dev libffi-dev

# Install app dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
# Using `pipenv` coz `pip` always lets me down installing from requirements.txt
# pip is dumb and tries to install windows only python packages in linux
# pipenv might be slow but gets the work done unlike fighting with pip
# PIPENV_VENV_IN_PROJECT=1 will create /.venv by default
RUN pip install pipenv \
    && PIPENV_VENV_IN_PROJECT=1 pipenv install --ignore-pipfile
# venv isn't necessary in docker image builds, but it can drastically 
# reduce build-times and produce optimised images in multi-stage builds


# STAGE 2
FROM python:3.9.12-alpine3.15

# Copy virtual env from STAGE 1
COPY --from=compile-time /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install application into container
COPY ./src /src
WORKDIR /src

EXPOSE 8080

# Run application
# DO NOT PASS `--preload` TO GUNICORN, IT IS CAUSING DEADLOCKs
CMD gunicorn -c gunicorn.conf.py "app:create_app()"