import redis

import secret

r = redis.StrictRedis(host=secret.HOST,
                      port=secret.PORT,
                      password=secret.PASSWORD)

p = r.pubsub()
p.subscribe('GAMEWORLD')

while True:
    for item in p.listen():
        print(item)
        print(item['data'])
