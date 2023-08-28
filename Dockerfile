FROM python:bullseye


COPY . .

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3" , "bot.py" ]