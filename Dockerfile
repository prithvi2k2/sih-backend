FROM python:3.9.12-alpine3.15

COPY . /src

WORKDIR /src

# Ensure installation of gcc and proper cffi bindings for working of Argon2
# This is heavily effecting build-time while building docker images,
# but also compensates it by providing security
RUN apk add gcc musl-dev libffi-dev \
    && pip install -U cffi pip wheel \
    # Also install production server WSGI packages and other requirements
    && pip install gunicorn eventlet \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD gunicorn -k eventlet -w 1 app:create_app