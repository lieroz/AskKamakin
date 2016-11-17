#!/bin/bash

sudo cp nginx.conf /etc/nginx/nginx.conf

if ps ax | grep -v grep | grep nginx > /dev/null
then
	sudo service nginx reload
else
	sudo service nginx start
fi

gunicorn -c ask_kamakin/gunicorn_conf.py hello

ab -c 10 -n 10000 http://localhost:8081/params > reports/gunicorn_wsgi_report.txt
ab -c 10 -n 10000 http://localhost:8081/ > reports/hello_wsgi_report.txt
ab -c 10 -n 10000 http://localhost/base.html > reports/nginx_static_report.txt
ab -c 10 -n 10000 http://localhost/params > reports/proxy_cache_report.txt
