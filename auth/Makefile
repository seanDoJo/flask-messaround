go : nginx py_deps conf_redis
	/usr/local/bin/uwsgi --ini preauth.ini

py_deps :
	yum install -y gcc
	yum install -y python35
	yum install -y python35-pip
	yum install -y python35-devel
	pip-3.5 install redis
	pip-3.5 install flask
	pip-3.5 install uwsgi

nginx :
	yum -y install nginx
	mkdir /var/www /var/www/bibe
	chown nginx:nginx /var/www/bibe
	service nginx stop
	cp nginx.conf.default /etc/nginx/nginx.conf
	service nginx start

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
