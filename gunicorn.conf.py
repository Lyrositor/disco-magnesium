from disco_magnesium.__main__ import LOG_CONFIG

wsgi_app = "disco_magnesium.api.app:setup_app"
bind = "127.0.0.1:1414"
logconfig_dict = LOG_CONFIG
worker_class = "uvicorn.workers.UvicornWorker"
workers = 4
