from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/admin/myhmbiz-api/gunicorn.sock'


# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'


# Logging Options
loglevel = 'debug'
accesslog = '/home/admin/myhmbiz-api/access_log'
errorlog =  '/home/admin/myhmbiz-api/error_log'