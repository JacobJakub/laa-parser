FROM sanjose/beautifulsoup

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD . .