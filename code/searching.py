# searching module
import time
from nltk.stem import PorterStemmer
from utils import stopwords
from score import getDocScore
#from readindex import readindex
import redis



stemmer = PorterStemmer()
rserver = redis.Redis('localhost')

def handle_field_query(query):
    b = query.split()
    f = None
    q = {}
    for word in b:
        if ":" in word:
            f = word[0]
        else:
            q[f] = []

    for word in b:
        if ":" in word:
            f = word[0]
        else:
            # normalize; case folding and stemming
            word = stemmer.stem(word.lower())
            q[f].append(word)
    return q


def normalize_query(query_string):
    query = []
    if ":" in query_string:
        # it's a field query
        # handle this
        q = handle_field_query(query_string)
        return q
    else:
        # case of normal query
        qlist = query_string.split()
        # case folding and stemming
        for term in qlist:
            query.append(stemmer.stem(term.lower()))
    return query


if __name__ == '__main__':
    print "setting up the search engine..."
    # indexfile = ""
    #readindex(rserver, indexfile)
    print "setup complete. search engine is ready.."
    while True:
        print "++++++++++++++++++++++++++++++++++++++"
        query_string = raw_input("Enter query: ")
        t = time.time()
        query_set = set(query_string.split())
        query_string = " ".join(list(query_set))
        q = normalize_query(query_string)
        if isinstance(q, dict):
            # it's a field query handle it
            qvalues = q.values()
            tempq = []
            for item in qvalues:
                tempq += item
            q = tempq
        # normal query
        df_list = []
        # contains (docid, tf_d)
        docinfo_list = {}
        for term in q:
            # get tok k posting list for each term and take union of them
            # ######get termid
            termid = rserver.hget('wordToId', term)
            # termid = id(term)
            if not termid:
                q.remove(term)
                continue
            docinfo_list[termid] = {}
            df = rserver.hget(termid, 'df')
            df_list.append(df)
            for docid in rserver.hkeys('d'+termid):
                # print "docid in redis:", docid
                tf_d = int(eval(rserver.hget('d'+termid, docid))[0])
                docinfo_list[termid][docid] = tf_d

        # at this point we have required info for each term
        # calculate score for each document based on these information
        # should contains doc socre in (docid, score)
        documents_score = []
        documentunion = set()
        # creating union of documents for query terms
        for qtid in docinfo_list:
            for docid in docinfo_list[qtid]:
                documentunion.add(docid)

        # for doc in docset
        # print "documentunion: ", documentunion
        for docid in documentunion:
            # get tf and doc len for each query term
            docInfo = []
            for qtid in docinfo_list:
                if docid in docinfo_list[qtid]:
                    tf = docinfo_list[qtid][docid]
                else:
                    tf = 0
                # get doc len; by default giving 1000
                d_len = 1000
                docInfo.append((tf, d_len))

            # get score for the document
            # assuming average document length as 1800
            avg_dl = 1800
            k = 1.5
            b = 0.75
            n = 53000
            ds = getDocScore(q, docInfo, df_list, avg_dl, k, b, n)
            documents_score.append((docid, ds))

        # short documents based on score
        documents_score.sort(key=lambda x:x[1], reverse=True)

        # print top 10 documents
        if len(documents_score) > 10:
            for i in xrange(10):
                # print documents_score
                docid = documents_score[i][0]
                title = rserver.hget('docidTotitle', docid)
                print title
        else:
            for i in xrange(len(documents_score)):
                # print documents_score
                docid = documents_score[i][0]
                title = rserver.hget('docidTotitle', docid)
                print title
        print "total time taken: ", time.time() - t
