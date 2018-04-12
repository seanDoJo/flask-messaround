go :
	ln -s ../utils utils
	/usr/bin/python35 utils/sql.py
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
	pip-3.5 install pymysql
	mkdir launch

clean :
	rm *.gz
