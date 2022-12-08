import multiprocessing
from os import getenv

port = getenv("PORT", "80")
bind = f"0.0.0.0:{port}"
max_workers = multiprocessing.cpu_count() * 2 + 1
workers = getenv("WORKERS", max_workers)
