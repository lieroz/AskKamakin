#!/bin/bash

sudo cp nginx.conf /etc/nginx/nginx.conf

if ps ax | grep -v grep | grep nginx > /dev/null
then
	sudo service nginx reload
else
	sudo service nginx start
fi

gunicorn -c ask_kamakin/gunicorn_conf.py hello
