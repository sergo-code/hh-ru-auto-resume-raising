FROM python:alpine


COPY . .

RUN apk add libxml2
RUN apk add libxslt-dev
RUN apk add libffi-dev
RUN apk add build-base

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3" , "bot.py" ]