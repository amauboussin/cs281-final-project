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
from load import all_subreddits_data, author_data
from prepare import tt_split, tokenize_all_words, tokens_to_vocab
from model import get_lda_models, lda_pred
from feature_selection import dirichlet_filter


all_data = author_data(20)

data = all_data
get_tokens = tokenize_all_words

train, test = tt_split(data)
print 'done splitting'
train_tokens = get_tokens(train)
print 'done tokenizing'
vocab = tokens_to_vocab(train_tokens)

train_tokens, removed = dirichlet_filter(train_tokens)
lda_models = get_lda_models(train_tokens, vocab, 100)


correct = 0
total = 0
for label, docset in test.iteritems():
    for doc in docset:
        total += 1
        if lda_pred(lda_models, vocab, doc) == label:
            correct += 1
print correct, total
