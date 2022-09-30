FROM ubuntu:latest as build
RUN apt update && apt install -y git
WORKDIR  /tmp
RUN git clone https://github.com/sergo-code/hh-ru-auto-resume-raising.git --branch main --depth 1

FROM python:3
RUN apt update && useradd -m hh -s /bin/bash
COPY --from=build /tmp/hh-ru-auto-resume-raising /home/hh/

COPY docker-entrypoint.sh /usr/local/bin
RUN chown -R hh:hh /home/hh && chmod 777 /usr/local/bin/docker-entrypoint.sh

USER hh
WORKDIR  /home/hh/
ENV PATH="${PATH}:/home/hh/.local/bin"
RUN pip install --upgrade pip && pip install -r requirements.txt

ARG PHONE='PHONE'
ARG PASSWORD='PASSWORD'
ARG PROXY='PROXY'
ARG BOT_TOKEN='BOT_TOKEN'
ARG ADMIN_TG='ADMIN_TG'
ARG TIME_ZONE='Europe/Moscow'

RUN echo "phone="${PHONE} > .env \
    && echo "password="${PASSWORD} >> .env \
    && echo "proxy="${PROXY} >> .env \
    && echo "bot_token="${BOT_TOKEN} >> .env \
    && echo "admin_tg="${ADMIN_TG} >> .env \
    && echo "time_zone="${TIME_ZONE} >> .env \
    && cat .env

ENTRYPOINT ["docker-entrypoint.sh"]
CMD [ "python3", "bot.py" ]
