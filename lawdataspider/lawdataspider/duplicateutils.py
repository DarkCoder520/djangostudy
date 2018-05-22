import hashlib

from .settings import redis_db

redis_findlaw_dict = "findlawurl"




def drop_duplicate_url(url):
    hl = hashlib.md5()
    hl.update(url.encode(encoding='utf-8'))
    md5 = hl.hexdigest()
    if redis_db.sismember(redis_findlaw_dict, md5):
        print("Duplicate url found:%s" % url)
        return True
    else:
        redis_db.sadd(redis_findlaw_dict,md5)
        return False


if __name__ == "__main__":
    drop_duplicate_url("http://xxxxx")