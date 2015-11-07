from collections import defaultdict
from funcy import partial
import unicodecsv as csv

from params import commenters, tv_subreddits

filepath = 'out.csv'
with open(filepath, 'rU') as rfile:
	reader = csv.DictReader(rfile)
	data = [r for r in reader]

def comments_list():
	return data

def group_by(collection, key):
	grouped = defaultdict(list)
	for row in collection:
		grouped[row[key]].append(row)
	return grouped

comments_grouped_by = partial(group_by, data)