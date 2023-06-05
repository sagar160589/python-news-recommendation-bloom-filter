import mmh3


class BloomFilter:
    def __init__(self, size, hashfn, redis_client):
        self.size = size
        self.hash_func = hashfn
        self.redis_client = redis_client

    def add(self, title):
        for seed in range(self.hash_func):
            index = mmh3.hash(title, seed) % self.size
            self.redis_client.setbit('news_bloom', index, 1)

    def exists(self, title):
        for seed in range(self.hash_func):
            index = mmh3.hash(title, seed) % self.size
            if self.redis_client.getbit('news_bloom', index) == 0:
                return False
        return True
