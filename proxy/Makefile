restart :
	service nginx stop
	cp nginx.conf.default /etc/nginx/nginx.conf
	sleep 1
	service nginx start

go : nginx py_deps
	/usr/local/bin/uwsgi --ini config.ini

py_deps :
	yum install -y gcc
	yum install -y python35
	yum install -y python35-pip
	yum install -y python35-devel
	pip-3.5 install flask
	pip-3.5 install uwsgi

nginx :
	yum -y install nginx
	mkdir /var/www /var/www/bibe
	chown nginx:nginx /var/www/bibe
	service nginx stop
	cp nginx.conf.default /etc/nginx/nginx.conf
	service nginx start
	mkdir conf

clean :
	rm *.gz
