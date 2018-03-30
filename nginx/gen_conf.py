import sys

data = sys.argv[1]
queue = sys.argv[2]

f_str = """
location {} {{
    include uwsgi_params;
    uwsgi_pass {}:{};

    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
}}
"""

with open("conf/data.conf", 'w+') as f:
    f.write(f_str.format("/data", data, 4242))

with open("conf/orders.conf", 'w+') as f:
    f.write(f_str.format("/orders/update", queue, 8080))
    f.write(f_str.format("/orders/get", queue, 8000))

