import hashlib, json, os, time

from flask_website import config


def create_key(unhashed):
    return hashlib.md5(unhashed.encode()).hexdigest()


def fetch_cache(cache_key, expiry = 3600):

    filename = '{dir}/{file}'.format(
        dir = config.cache_dir,
        file = cache_key)

    # file exists?
    if os.path.isfile(filename) == False:
        return False

    # expired?
    if (time.time() - os.path.getctime(filename)) > expiry:
        return False

    # return contents of key
    return json.loads(open(filename, 'r').read().rstrip())

def write_cache(cache_key, data):

    filename = '{dir}/{file}'.format(
        dir = config.cache_dir,
        file = cache_key)

    with open(filename, 'w+') as f:
        print(json.dumps(data), file=f)
    return True
