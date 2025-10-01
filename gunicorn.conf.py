# Gunicorn configuration file
bind = "0.0.0.0:5000"
timeout = 180  # 3 minutes timeout for long AI processing
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
reload = True
reuse_port = True