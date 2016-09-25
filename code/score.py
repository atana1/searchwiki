# Module for calculating score of a document
# Okapi BM25 is used for score calculation
import math


def getIDF(term, n, df):
    """ returns IDF of a term.
        n is total number of documents
        df is document frequency
    """
    # print "df is ", df
    num = n - df + 0.5
    denom = df + 0.5
    return math.log10(num/float(denom))


def okapiBM25score(qterm, docInfo, df, tf_d, k, b, n):
    """ given query term and document(doc info) it
        returns okapi score of a document
        docInfo is a tuple containing (D_len, avg_dl)
    """
    D_len, avg_dl = docInfo

    num = tf_d * (k + 1)
    denom = tf_d + k * ((1 - b) + b * (D_len/float(avg_dl)))
    score = getIDF(qterm, n, df) * (num/float(denom))
    return score


def getDocScore(query, docsInfo_list, df_list, avg_dl, k, b, n):
    """ returns doc score for given query.
        k and b are okapi parameters and n is
        total documents in collection. query
        contains list of normalized query
        terms. docInfo_list is a list of tuple containing
        [(tf_d, D_len), (tf_d, D_len), ..]
    """
    score = 0.0
    i = 0
    for qterm in query:
        # get document length
        tf_d, D_len = docsInfo_list[i]
        docInfo = (D_len, avg_dl)
        score += okapiBM25score(qterm, docInfo, int(df_list[i]), tf_d, k, b, n)
        i += 1
    return score
