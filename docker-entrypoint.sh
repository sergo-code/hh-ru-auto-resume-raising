#!/bin/bash

# docker-entrypoint.sh

if [ -n "$PHONE" ]; then
    sed -i 's/PHONE/'"$PHONE"'/g' /home/hh/.env
fi

if [ -n "$PASSWORD" ]; then
    sed -i 's/PASSWORD/'"$PASSWORD"'/g' /home/hh/.env
fi

if [ -n "$PROXY" ]; then
    sed -i 's/PROXY/'"$PROXY"'/g' /home/hh/.env
fi

if [ -n "$BOT_TOKEN" ]; then
    sed -i 's/BOT_TOKEN/'"$BOT_TOKEN"'/g' /home/hh/.env
fi

if [ -n "$ADMIN_TG" ]; then
    sed -i 's/ADMIN_TG/'"$ADMIN_TG"'/g' /home/hh/.env
fi

if [ -n "$TIME_ZONE" ]; then
sed -i 's/Europe\/Moscow/'"$TIME_ZONE"'/g' /home/hh/.env
fi


exec "$@"
