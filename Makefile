status_redis :
	cat /var/log/redis_6379.log

stop_redis :
	/etc/init.d/redis_6379 stop

start_redis :
	/etc/init.d/redis_6379 start

run :
	export FLASK_APP=app.py && flask run

py_deps :
	pip3 install redis
	pip3 install flask
	apt-get install python3-flask

conf_redis : build_redis
	mkdir -p /etc/redis
	mkdir -p /var/redis
	cp redis/redis_init_script /etc/init.d/redis_6379
	cp redis/redis.conf /etc/redis/6379.conf
	mkdir -p /var/reds/6379
	update-rc.d redis_6379 defaults
	rm -rf redis-stable

build_redis : 
	wget http://download.redis.io/redis-stable.tar.gz
	tar xzvf redis-stable.tar.gz
	rm redis-stable.tar.gz
	cd redis-stable/deps && make hiredis lua jemalloc linenoise
	cd redis-stable && make && make install

clean :
	rm *.gz
