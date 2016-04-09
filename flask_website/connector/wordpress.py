import json, requests

from flask_website import config
from flask_website.connector import filecache


def get_user_posts (ids, expiry = None):
    cache_key = filecache.create_key(ids)

    # cache requested?
    if expiry != None:
        data = filecache.fetch_cache(cache_key, expiry)
        if data != False:
            return data

    if ids != None:
        ids = ids.split(',')

    # import pdb; pdb.set_trace()
    data = []
    for i in ids:
        url = '{base_url}/wp-json/wp/v2/posts/{id}'.format(
                    base_url=config.wordpress.get('base_url'),
                    id=i)
        post = requests.get(url).json()
        if post.get('featured_image') > 0:
            url = '{base_url}/wp-json/wp/v2/media/{id}'.format(
                        base_url=config.wordpress.get('base_url'),
                        id=post.get('featured_image'))
            media = requests.get(url).json()
            post['featured_image'] = media
        data.append(post)

    # write to cache
    filecache.write_cache(cache_key, data)
    return data
