# from multiprocessing import pool
import redis

# r = redis.StrictRedis(host='81.68.92.89',port=6379, db=0,password='******')
# r.set('hot', '1')

# print(r.ping())
# print(r.set("hpj","crr"))
# print(r.get('hpj'))
# r.set('times', '1')
# for i in range(100):
#     r.incr('times', 1)
#     print(r.get('times'))

Pool = None

def getredis():
    #用作返回一个可以操作的redis对象
    global Pool 
    if not Pool:
        Pool = redis.ConnectionPool(host='81.68.92.89', port=6379,password='*******',max_connections=10,db=0)
    return redis.Redis(connection_pool=Pool)

