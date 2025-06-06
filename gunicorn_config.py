bind = "unix:/tmp/megatrip.sock"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"

# Ensure proper permissions for the Unix socket
user = "www-data"
group = "www-data"

# Additional recommended settings
capture_output = True
enable_stdio_inheritance = True 