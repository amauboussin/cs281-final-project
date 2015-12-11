from connect import get_rows, query_to_csv
from params import askreddit_commenters, all_subreddits

# print '\n'.join(map(lambda x: x[0], get_rows('select subreddit from May2015 group by subreddit order by count(*) desc limit 200')))

# print '\n'.join(map(lambda x: x[0], get_rows('select author from May2015 where subreddit = \'AskReddit\' group by author order by count(*) desc limit 50')))


where_in_top = ' or '.join(['subreddit = "%s"' % s for s in all_subreddits])
where_by_uname = ' or '.join(['author = "%s"' % s for s in askreddit_commenters])

# subreddit_data = 'select author, subreddit, score, ups, downs, link_id, created_utc, body from May2015 where (%s)' % where_in_top
# query_to_csv(subreddit_data, 'subreddit_data.csv')

# author_data = 'select author, subreddit, score, ups, downs, link_id, created_utc, body from May2015 where (subreddit = \'AskReddit\' and (%s))' % where_by_uname
# query_to_csv(author_data, 'author_data.csv')


subreddit_q = 'select author, subreddit, score, ups, downs, link_id, created_utc, body from May2015 where subreddit = \'[subreddit]\' order by RANDOM() limit 100000'
sr_query = lambda sr: subreddit_q.replace('[subreddit]', sr)
for subreddit in reversed(all_subreddits):
	query_to_csv(sr_query(subreddit), 'data/%s.csv' % subreddit)



# subreddit_data = 'select author, subreddit, score, ups, downs, link_id, created_utc, body from May2015 where (%s)' % where_in_top
# query_to_csv(subreddit_data, 'author_data.csv')
