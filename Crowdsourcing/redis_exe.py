import os
import redis


class Redis_Handler:
    def __init__(self):
        self.redis_client = redis.Redis(host=os.environ.get("REDIS_HOST"),
                                        port=os.environ.get("REDIS_PORT_NUMBER"),
                                        db=os.environ.get("REDIS_DB_NUMBER", 0))
    
    def add(self, set_name, expire_time, value):
        self.redis_client.setex(set_name, expire_time, value)
    
    def remove(self, set_name, value):
        self.redis_client.srem(set_name, value)
    
    def get_user(self, set_name):
        return self.redis_client.get(set_name)


Redis = Redis_Handler()