.PHONY: nginx

restart :
	service nginx stop
	cp nginx/nginx.conf.default /etc/nginx/nginx.conf
	sleep 1
	service nginx start

nginx :
	yum install -y nginx
	mkdir /var/www /var/www/bibe
	chown nginx:nginx /var/www/bibe
	service nginx stop
	cp nginx/nginx.conf.default /etc/nginx/nginx.conf
	service nginx start

clean :
	rm *.gz
