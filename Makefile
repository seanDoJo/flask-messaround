.PHONY: nginx

status_redis :
	cat /var/log/redis_6379.log

stop_redis :
	/etc/init.d/redis_6379 stop

start_redis :
	/etc/init.d/redis_6379 start

run :
	export FLASK_APP=app.py
	uwsgi --socket 127.0.0.1:4242 --module app --callab app

go : nginx py_deps conf_redis
	uwsgi --ini config.ini

nginx :
	yum install nginx
	service nginx stop
	cp nginx/nginx.conf.default /etc/nginx/nginx.conf
	service nginx start

py_deps :
	yum install gcc
	yum install python35
	yum install python35-pip
	yum install python35-devel
	pip-3.5 install redis
	pip-3.5 install flask
	pip-3.5 install uwsgi 

conf_redis : build_redis
	mkdir /etc/redis
	mkdir /var/redis
	cp redis/redis_init_script /etc/init.d/redis_6379
	cp redis/redis.conf /etc/redis/6379.conf
	mkdir /var/reds/6379
	/etc/init.d/redis_6379 start
	rm -rf redis-stable

build_redis : 
	wget http://download.redis.io/redis-stable.tar.gz
	tar xzvf redis-stable.tar.gz
	rm redis-stable.tar.gz
	cd redis-stable/deps && make hiredis lua jemalloc linenoise
	cd redis-stable && make && make install

clean :
	rm *.gz
