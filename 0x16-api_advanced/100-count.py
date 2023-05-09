#!/usr/bin/python3

'''
A module containing functions for working with the Reddit API.
'''

import requests

def sort_histogram(histogram={}):
    '''
    Sorts and prints the given histogram.
    '''
    histogram = list(filter(lambda kv: kv[1], histogram))
    histogram_dict = {}
    for item in histogram:
        if item[0] in histogram_dict:
            histogram_dict[item[0]] += item[1]
        else:
            histogram_dict[item[0]] = item[1]
    histogram = list(histogram_dict.items())
    histogram.sort(
        key=lambda kv: kv[0],
        reverse=False
    )
    histogram.sort(
        key=lambda kv: kv[1],
        reverse=True
    )
    res_str = '\n'.join(list(map(
        lambda kv: '{}: {}'.format(kv[0], kv[1]),
        histogram
    )))
    if res_str:
        return res_str


def count_words(subreddit, word_list, histogram=None, n=0, after=None):
    '''
    Counts the number of times each word in a given wordlist
    occurs in a given subreddit.
    '''
    if histogram is None:
        histogram = [(word, 0) for word in word_list]
    api_headers = {
        'User-Agent': 'my_bot/0.1'  # Replace with your own User-Agent string
    }
    sort = 'hot'
    limit = 30
    res = requests.get(
        '{}/r/{}/.json?sort={}&limit={}&count={}&after={}'.format(
            'https://www.reddit.com',
            subreddit,
            sort,
            limit,
            n,
            after if after else ''
        ),
        headers=api_headers,
        allow_redirects=False
    )
    if res.status_code == 200:
        data = res.json()['data']
        posts = data['children']
        titles = [post['data']['title'] for post in posts]
        histogram = [
            (word, count + sum(
                txt.lower().split().count(word)
                for txt in titles
            )) for (word, count) in histogram
        ]
        if len(posts) >= limit and data['after']:
            return count_words(
                subreddit,
                word_list,
                histogram,
                n + len(posts),
                data['after']
            )
        else:
            return histogram


if __name__ == '__main__':
    print(__doc__)

