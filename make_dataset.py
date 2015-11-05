from connect import get_rows, query_to_csv
from params import commenters, tv_subreddits

where_in_tv = ' or '.join(['subreddit = "%s"' % s for s in tv_subreddits])
comments_by_subreddit = 'select subreddit, count(*) from May2015 where %s group by subreddit order by count(*) desc' % where_in_tv
comments_by_author = 'select author, count(distinct subreddit), count(*) from May2015 where %s group by author order by count(*) desc limit 1000' % where_in_tv

usernames = map(lambda x : x[0], commenters)
where_by_uname = ' or '.join(['author = "%s"' % s for s in usernames])

comment_dump = 'select author, subreddit, score, downs, created_utc, body from May2015 where ((%s) and (%s))' % (where_in_tv, where_by_uname)


query_to_csv(comment_dump, 'out.csv')

