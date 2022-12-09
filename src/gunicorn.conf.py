from config import gunicorn_config

bind = f"0.0.0.0:{gunicorn_config.port}"
workers = gunicorn_config.count_workers
