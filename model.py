import numpy as np
from nltk import word_tokenize
import gensim as gs
from sklearn.feature_extraction.text import CountVectorizer
import lda

from prepare import word_tokenize_doc

def get_hlda_models(train_tokens, vocab, n_topics=40):
    models = {}
    dictionary = gs.corpora.Dictionary(map(lambda x: [x], vocab.keys()))
    for label, docs in train_tokens.items():
        corpus = [dictionary.doc2bow(d) for d in docs]
        models[label] = gs.models.HdpModel(corpus, dictionary, T=n_topics)
    return models, dictionary

def get_lda_models(train_tokens, vocab, n_topics=40):
    all_models = {}
    def fit_model((label, docs)):
        model = lda.LDA(n_topics=n_topics, n_iter=200)
        vectorizer = CountVectorizer(min_df=2, vocabulary = vocab, stop_words=None)
        X = vectorizer.fit_transform(map(lambda s: ' '.join(s), docs))
        model.fit(X)
        all_models[label] = model
        print 'done fitting for ', label
    map(fit_model, train_tokens.items())
    return all_models


def get_lda_models_spectral(train_tokens, vocab, n_topics=40):
    all_models = {}
    def fit_model((label, docs)):
        model = lda.LDA(n_topics=n_topics, n_iter=200)
        vectorizer = CountVectorizer(min_df=2, vocabulary = vocab, stop_words=None)
        X = vectorizer.fit_transform(map(lambda s: ' '.join(s), docs))
        model.fit(X)
        all_models[label] = model
        print 'done fitting for ', label
    map(fit_model, train_tokens.items())
    return all_models

def hlda_pred(models, dictionary, doc):
    corpus = [dictionary.doc2bow(word_tokenize_doc(doc))]
    label_score = []
    for label, hdp in models.iteritems():
        label_score.append((label, hdp.evaluate_test_corpus(corpus)))
    return max(label_score, key = lambda x:x[1])[0]

def lda_pred(models, vocab, doc):
    """Get a class prediction for a document """
    tokenized = word_tokenize_doc(doc)
    vectorizer = CountVectorizer(min_df=1, vocabulary = vocab, stop_words=None)
    X = vectorizer.fit_transform([' '.join(tokenized)])
    label_score = []
    for label, model in models.iteritems():
        n_topics = len(model.components_)
        topic_dist = model.transform(X)
        log_likelihood = 0
        for token in tokenized:
            if token in vocab:
                max_likelihood = -1 * 10 ** 8
                for topic in range(n_topics):
                    ll = np.log(model.components_[topic][vocab[token]]) + np.log(topic_dist[0][topic])
                    max_likelihood = max_likelihood if max_likelihood > ll else ll
                log_likelihood += max_likelihood
        label_score.append((label, log_likelihood))
    return max(label_score, key = lambda x:x[1])[0]