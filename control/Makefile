restart :
	service nginx stop
	cp nginx.conf.default /etc/nginx/nginx.conf
	sleep 1
	service nginx start

go : py_deps
	/usr/bin/python35 sql.py
	/usr/bin/python35 create.py &
	/usr/local/bin/uwsgi --ini config.ini

py_deps :
	yum install -y gcc
	yum install -y python35
	yum install -y python35-pip
	yum install -y python35-devel
	pip-3.5 install flask
	pip-3.5 install uwsgi
	pip-3.5 install requests
	pip-3.5 install sqlalchemy
	mkdir launch

clean :
	rm *.gz
