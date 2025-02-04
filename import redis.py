import redis
r = redis.Redis(host='localhost', port=32768, db=0)


r.set('user:1:name', 'John Doe')
r.set('user:1:email', 'john.doe@example.com')

r.setex('session_key', 3600, 'session_data')

user_name = r.get('user:1:name')
user_email = r.get('user:1:email')

user_name = user_name.decode('utf-8')
user_email = user_email.decode('utf-8')


keys = ['user:1:name', 'user:1:email']
values = r.mget(keys)
# Convert byte values to strings
values = [value.decode('utf-8') for value in values]




import redis
from redis import ConnectionPool

pool = ConnectionPool(host='localhost', port=32768, db=0)
r = redis.Redis(connection_pool=pool)

pool = ConnectionPool(host='localhost', port=32768, db=0)

r1 = redis.Redis(connection_pool=pool)
r2 = redis.Redis(connection_pool=pool)

import threading

pool = ConnectionPool(host='localhost', port=32768, db=0)

def worker():
    r = redis.Redis(connection_pool=pool)
    # Perform Redis operations with 'r'

threads = [threading.Thread(target=worker) for _ in range(5)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
    
    

pool = ConnectionPool(
    host='localhost',
    port=32768,
    db=0,
    max_connections=10,
    timeout=5,
    socket_connect_timeout=3,
    socket_keepalive=True
)
r = redis.Redis(connection_pool=pool)

