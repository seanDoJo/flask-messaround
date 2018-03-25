.PHONY: nginx
nginx :
	yum install nginx
	service nginx stop
	cp nginx/nginx.conf.default /etc/nginx/nginx.conf
	service nginx start

clean :
	rm *.gz
