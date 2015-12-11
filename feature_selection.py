from collections import defaultdict
import numpy as np
from scipy.stats import dirichlet




def normalize(v):
    return v / float(np.sum(v))

def score_words(train_tokens):

    words = set()
    all_counts = {}
    for label, docs in train_tokens.iteritems():
        counts = defaultdict(int)
        for d in docs:
            for t in d:
                counts[t] += 1
                words.add(t)
        all_counts[label] = counts


    # d filter
    word_score = []
    for w in words:
        get_count = lambda d: d.get(w, 0)

        x = normalize(np.array(map(get_count, all_counts.values())))
        score = dirichlet.logpdf(normalize(x), np.ones(len(all_counts)) * 2)
        word_score.append((w, score))
    return word_score


def dirichlet_filter(train_tokens, threshold = 20):

    word_scores = score_words(train_tokens)

    words_to_remove = set(map(lambda x:x[0], filter(lambda x: x[1] > threshold, word_scores)))

    keep_word = lambda w: w not in words_to_remove

    removed = 0

    for label, docs in train_tokens.iteritems():
        for i in range(len(docs)):
            old_length = len(docs[i])
            docs[i] = filter(keep_word, docs[i])
            removed += old_length - len(docs[i])
        train_tokens[label] = docs

    return train_tokens, removed
            






