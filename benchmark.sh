ab -c 10 -n 10000 http://localhost:8081/params > reports/gunicorn_wsgi_report.txt
ab -c 10 -n 10000 http://localhost:8081/ > reports/hello_wsgi_report.txt
ab -c 10 -n 10000 http://localhost/base.html > reports/nginx_static_report.txt
ab -c 10 -n 10000 http://localhost/params > reports/proxy_cache_report.txt

sudo service nginx stop
