import string
#from stemming.porter2 import stem
from nltk.stem import PorterStemmer
from utils import stopwords


stemmer = PorterStemmer()

def tokenize(text):
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    replace_punctuation = string.maketrans(string.punctuation,
                                           ' '*len(string.punctuation))
    out = text.translate(replace_punctuation)
    out = out.split()
    #stemmed_words = [stemmer.stem(word.lower().decode('utf-8')) for word in out if word.lower().decode('utf-8') not in stopwords]
    stemmed_words = []
    for word in out:
	tmpword = word.lower().decode('utf-8')
	if len(tmpword)> 2 and tmpword not in stopwords:
	    # print tmpword.encode('utf-8')
	    tmpword = ''.join(i for i in tmpword if not i.isdigit())
	    stemmedword = stemmer.stem(tmpword)
	    if stemmedword not in stopwords and len(stemmedword) > 2:
		# print stemmedword
		#if u'\u4e00' <= stemmedword[0] <= u'\u9fff' or u'\u4e00' <= stemmedword[1] <= u'\u9fff':
		#    continue
		stemmed_words.append(stemmedword)
    return stemmed_words

