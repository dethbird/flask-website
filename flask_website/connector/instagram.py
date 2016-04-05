import json, requests

from flask_website import config

def get_user_posts (user_id, count, tags = None):
    """Get a user's Instagram posts.

    Filter by tags and and max $count items.

    Returns:
        Response: the JSON items representing instagram posts.
    """
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
    return data
