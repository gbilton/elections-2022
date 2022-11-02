from rq import Queue  # type: ignore
from redis import Redis
from backend.app.config import settings


host = settings["REDIS_HOST"]
port = settings["REDIS_PORT"]

# Tell RQ what Redis connection to use
redis_conn = Redis(host=host, port=port)
worker = Queue(connection=redis_conn)  # no args implies the default queue
