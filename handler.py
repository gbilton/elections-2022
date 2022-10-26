from rq import Queue  # type: ignore
from redis import Redis

# Tell RQ what Redis connection to use
redis_conn = Redis()
worker = Queue(connection=redis_conn)  # no args implies the default queue
