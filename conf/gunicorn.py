from mlservefast.config import logfile_path


logconfig = logfile_path(debug=False)
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
preload_app = False
