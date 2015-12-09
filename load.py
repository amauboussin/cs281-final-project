from collections import defaultdict
from functools import partial
from funcy import pluck
import os
import unicodecsv as csv

import numpy as np
from params import commenters, tv_subreddits

tv_file = 'out.csv'
all_sr_dir = 'data/'
author_file = 'author_data.csv'

def read_file(filepath):
    with open(filepath, 'rU') as rfile:
        reader = csv.DictReader(rfile)
        data = [r for r in reader]
    return data

def tv_comments_list():
    return read_file(tv_file)

def group_by(collection, key):
    grouped = defaultdict(list)
    for row in collection:
        grouped[row[key]].append(row)
    return grouped

def tv_comments_grouped_by(group_by_key):
    return group_by(read_file(tv_file), group_by_key)



def pool_n(n, comments):
    """Pool every n comments"""
    pool = lambda comments: ' '.join(pluck('body', comments))
    pools = []
    for i in range(0, len(comments), n):
        pools.append(pool(comments[i: min(len(comments), i+n)]))
    if len(pools[-1]) < n:
        pools = pools[:-1]
    return pools

def tv_subreddits_data(n=10, pool_every=40, sort_by='created_utc'):
    by_subreddit = tv_comments_grouped_by('subreddit')
    k_n_data = []
    for sr, comments in by_subreddit.items():
        n_comments = len(comments)
        k_n_data.append((sr, n_comments, comments))

    k_n_data = sorted(k_n_data, key = lambda (k, n, d): n, reverse=True)[:n]
    pooled = {}
    for (sr, n, comments) in k_n_data:
        pooled[sr] = pool_n(pool_every, comments)
    
    print len(pooled)
    return pooled


def all_subreddits_data(n=30, per_subreddit=1000, min_comments=10):
    subreddits = {f.split('.')[0] : read_file(os.path.join(all_sr_dir, f)) for f in os.listdir(all_sr_dir)}
    filtered_subreddits = {}
    k_mean_data = []
    for k, comments in subreddits.items():
        grouped = group_by(comments, 'link_id')
        mean_comments = np.mean(map(len, grouped.values()))
        k_mean_data.append((k, mean_comments, grouped))
    
    k_mean_data = sorted(k_mean_data, key = lambda (k, m, d): m, reverse=True)[:n]
    for (k, mean, data) in k_mean_data:
        filtered_data = {}
        for d, comments in data.items():
            if len(comments) > 10:
                filtered_data[d] = ' '.join([c['body'] for c in comments])
        filtered_subreddits[k] = filtered_data.values()
    
    return filtered_subreddits

def author_data(pool_every=30):
    data = read_file(author_file)
    grouped = group_by(data, 'author')
    pooled = {}
    for author, comments in grouped.iteritems():
        pooled[author] =  pool_n(pool_every, sorted(comments, key = lambda c: c['created_utc']))
    return pooled

def main():
    author_data()

#  main method for testing
if __name__ == '__main__':
    main()
