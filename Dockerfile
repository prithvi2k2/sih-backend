FROM python:3.9.12-alpine3.15

COPY . /src

WORKDIR /src

# Ensure installation of gcc and proper cffi bindings for working of Argon2
# This is heavily effecting build-time while building docker images,
# but also compensates it by providing security
RUN apk add gcc musl-dev libffi-dev \
    && pip install -U cffi pip setuptools

# Install requirements
RUN pip install -r requirements.txt

EXPOSE 8080

# This command is specifically for Heroku, because of how differently it treats Dockerfiles
# It ignores EXPOSE commands and we don't see any other way to PUBLISH ports except below
# Here, $PORT is pre-defined env var by Heroku
CMD python prod_server.py