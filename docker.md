# Head hanter bot

docker-compose.yaml
```
version: '3.8'
services:

  hh:
    container_name: hh
    environment:
      PHONE: '79876543210'
      PASSWORD: 'qwerty123'
      PROXY: 'None or http://login:password@ip:port'
      BOT_TOKEN: '1111111:a1a1a1a1a1a'
      ADMIN_TG: '01020304'
    image: hub.polmira.ru/polmira/hh-ru-auto-resume:latest
    restart: unless-stopped
```
