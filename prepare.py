import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.cross_validation import train_test_split


def tt_split(data, test_size=.1):
    """Splits a dictionary {class_label: list of documents}"""
    """into two dictionaries of the same shape"""
    train_data = {}; test_data = {}
    for label, docs in data.iteritems():
        train, test = train_test_split(docs, test_size=test_size)
        train_data[label] = train
        test_data[label] = test
    return train_data, test_data

def tokens_to_vocab(class_tokens):
    """{class_label : list of tokenized documents} -> vocab"""
    vocab = set([])
    for _class, tokenized_docs in class_tokens.iteritems():
        for d in tokenized_docs:
            vocab = vocab.union(set(d))
    return {word: i for i, word in enumerate(vocab)}
        

def word_tokenize_doc(doc):
    """Word tokenize a single document"""
    to_remove = set(['http', 'faq', 'https', 'amp','source', 'deletion', 'sfw',
              'nsfw', 'gt', 'gon', 'na', 'delete', 'comment', 'profile'])
    def _filter(w):
        return all([w.isalnum(), w not in stopwords.words('english'), w not in to_remove])
    tokens = word_tokenize(doc)
    tokens = filter(_filter, tokens)
    return tokens

def tokenize_all_words(data):
    """basic get_tokens method"""
    """{class_label: list of documents} ->""" 
    """{class_label : list of tokenized documents}"""
    for c, docs in data.iteritems():
        data[c] = map(word_tokenize_doc, docs)
    return data


def clean(data):
    """Returns train, test, trian_tokens, vocab"""
    train, test = tt_split(data)
    print 'done splitting'
    train_tokens = tokenize_all_words(train)
    print 'done tokenizing'
    vocab = tokens_to_vocab(train_tokens)
    return train, test, train_tokens, vocab


