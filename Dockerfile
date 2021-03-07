FROM python:3.9

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libmariadb-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim

WORKDIR /code

RUN pip install -U pip pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile


STOPSIGNAL SIGINT
ENTRYPOINT [ "daphne", "back.asgi:application" ]
#CMD [ "runserver", "0.0.0.0:8000" ]

