#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import tweepy
from importd import d
import os

try:
    import config
    API_KEY = config.API_CLIENT_KEY
    SECRET_KEY = config.API_SECRET_KEY
except:
    API_KEY = os.environ['TWITTER_API_KEY']
    SECRET_KEY = os.environ['TWITTER_SECRET_KEY']

def get_score(user):
    elem_list = [
        user.statuses_count * 1,
        user.friends_count * 1,
        user.followers_count * 1,
        user.favourites_count * 1
    ]
    total = int(sum(elem_list))

    return {
        'status': user.statuses_count,
        'following': user.friends_count,
        'follower': user.followers_count,
        'favorite': user.favourites_count,
        'score': total,
        'screen_name': user.screen_name
    }

def get_score_table(screen_name_list):
    auth = tweepy.OAuthHandler(API_KEY, SECRET_KEY)
    api = tweepy.API(auth)

    retval = []
    for screen_name in screen_name_list:
        try:
            user = api.get_user(screen_name=screen_name)
            score = get_score(user)
        except tweepy.error.TweepError:
            score = -1
        retval.append(score)
    return retval

def sort_no_answer(username_list):
    score_list = get_score_table(username_list)
    score_list = sorted(score_list, key=lambda x: x['score'], reverse=True)
    return score_list

d(
    DEBUG=True,
    INSTALLED_APPS=(
    ),
    DEFAULT_JINJA2_TEMPLATE_EXTENSION='.jinja2',
)

@d('/')
def view_index(request):
    if request.method == 'GET':
        username_list = ['if1live', 'foo', 'bar']
        result = []
    else:
        username_list = request.POST['names'].splitlines()
        username_list = [x for x in username_list if len(x) > 0]
        result = sort_no_answer(username_list)

    ctx = {
        'usernames': '\n'.join(username_list),
        'result': result
    }
    return d.render_to_response('index.jinja2', ctx)

if __name__ == '__main__':
    d.main()
