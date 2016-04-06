import json, requests

from flask_website import config
from flask_website.connector import filecache


def get_user_posts (user_id, count, tags = None, expiry = None):
    """Get a user's Instagram posts.

    Filter by tags and and max $count items.

    Returns:
        Response: the JSON items representing instagram posts.
    """

    # create the cache key
    cache_key = filecache.create_key('{user_id}{count}{tags}'.format(
        user_id = user_id,
        count = count,
        tags = tags))

    # cache requested?
    if expiry != None:
        data = filecache.fetch_cache(cache_key, expiry)
        if data != False:
            return data

    # type casting
    count = int(count)
    if tags != None:
        tags = tags.split(',')

    url = None
    data = []
    while len(data) < count:
        if url == None:
            url = (
                'https://api.instagram.com/v1/users/{user_id}'
                '/media/recent/?client_id={client_id}&count={count}').format(
                    user_id=user_id,
                    client_id=config.instagram.get('client_id'),
                    count=count)

        response = requests.get(url).json()
        posts = response.get('data')
        for post in posts:
            if len(data) < count:
                # no tag filtering requested
                if tags == None:
                    data.append(post)
                # tags requested
                else:
                    for tag in tags:
                        if post.get('tags').count(tag) > 0:
                            data.append(post)
                            break
            else:
                break
        url = response.get('pagination').get('next_url')

    # write to cache
    filecache.write_cache(cache_key, data)
    return data
