kill :
	kill -9 `cat /tmp/bibe_reader.pid`
	kill -9 `cat /tmp/bibe_writer.pid`
	rm -rf __pycache__
	rm utils

run :
	ln -s ../utils utils
	uwsgi --ini write.ini
	uwsgi --ini read.ini

go : py_deps conf_redis
	/usr/local/bin/uwsgi --ini write.ini
	/usr/local/bin/uwsgi --ini read.ini

py_deps :
	yum install -y gcc
	yum install -y python35
	yum install -y python35-pip
	yum install -y python35-devel
	pip-3.5 install redis
	pip-3.5 install flask
	pip-3.5 install uwsgi 
	pip-3.5 install requests

conf_redis : build_redis
	mkdir /etc/redis
	mkdir /var/redis
	cp ../redis/redis_init_script /etc/init.d/redis_6379
	cp ../redis/redis.conf /etc/redis/6379.conf
	mkdir /var/redis/6379
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
