from utils import WordLexicon, bags
# A class that summarizes a document in form of tokens
# Bag of words representation

outputfile = open("index.txt", "wa")
i = 0
#bags = []
class DocumentSummarizer(object):
    def summarize(self, docId, docInfo):
	""" takes a docInfo list that contains list tuples
	    (fields, ptokens)
	"""
	doc_summary = {}
	word_summary = {}
        global i
	for fields, ptokens in docInfo:
	    for tok in ptokens:
		if len(tok) < 3:
			continue
		# print tok.encode('utf-8')
		# create null dict for all the key(word)
		if tok not in WordLexicon:
		    WordLexicon[tok] = i
		    i += 1
		wordId = WordLexicon[tok]
		#word = tok
		#if word not in word_summary:
		#    word_summary[word] = {} 
		if wordId not in word_summary:
		    word_summary[wordId] = {}
		
		for f in fields:
		    #word_summary[word][f] = word_summary[word].get(f, 0) + 1	
		    word_summary[wordId][f] = word_summary[wordId].get(f, 0) + 1
	
	# make tokens and summarize
	for word in word_summary:
	    #fields = [(f, word_summary[word][f]) for f in word_summary[word]]
	    token = []
	    #token.append(word)
	    #token.append(" ")
	    #token.append(docId)
	    #token.append(" ")
	    for field in word_summary[word]:
		token.append(field)
		token.append(str(word_summary[word][field]))
	    #token.append("\n")
	    token = "".join(token)
	    newtok = (word, docId, token)
	    bags.append(newtok)
	    #print token
	    #outputfile.write(token.encode('utf-8'))
	    #print "%s %s %s" %(word, docId, fields)


#testdata = [(['T', 'B', 'C'], ['The', 'cat', 'is']), (['B', 'C'], ['The', 'world', 'is'])]
#testdata2 = [(['T', 'B', 'C'], ['The', 'owl', 'is']), (['B', 'C'], ['The', 'world', 'is'])]
#ds = DocumentSummarizer()
#ds.summarize(108, testdata)
#ds.summarize(108, testdata2)		
