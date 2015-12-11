import cPickle as pickle
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import gensim as gs
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import lda
from load import all_subreddits_data, tv_subreddits_data

from model import get_lda_models, lda_pred

from feature_selection import dirichlet_filter



pickle_filepath = 'cache/data.pickle'

def load():
    with open(pickle_filepath, 'r') as rfile:
        train, test, train_tokens, vocab = pickle.load(rfile)
    return train, test, train_tokens, vocab
    
train, test, train_tokens, vocab = load()

train_tokens, removed = dirichlet_filter(train_tokens)
lda_models = get_lda_models(train_tokens, vocab, 40)


correct = 0
total = 0
for label, docset in test.iteritems():
    for doc in docset:
        total += 1
        if lda_pred(lda_models, vocab, doc) == label:
            correct += 1
print correct, total