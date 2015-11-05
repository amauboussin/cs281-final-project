import unicodecsv as csv
import sqlite3

path = '/Volumes/ExFat 1/database.sqlite'
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row
c = conn.cursor()


# movies, music, sports (nba, nfl, hockey) games (league of legends, starcraft)

#  column keys for reference
keys = ['created_utc', 'ups', 'subreddit_id', 'link_id', 'name', 'score_hidden', 
'author_flair_css_class', 'author_flair_text', 'subreddit', 'id', 'removal_reason',
'gilded', 'downs', 'archived', 'author', 'score', 'retrieved_on',
'body', 'distinguished', 'edited', 'controversiality', 'parent_id']


def get_rows(query):
	return c.execute(query).fetchall()

def query_to_csv(query, filename):
	data = c.execute(query)
	with open(filename, 'w') as wfile:
		writer = csv.writer(wfile)
		writer.writerow([d[0] for d in data.description])
		for row in data:
			writer.writerow(row)

