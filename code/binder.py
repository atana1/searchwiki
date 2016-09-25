from collections import deque
from utils import content_queue, summarize_queue
from mytokenizer import tokenize
from documentsummarizer import DocumentSummarizer


#tk = Tokenizer()
# test_data = [1, (0, ['T', 'B'], 'My text'), 0, 1, (1, ['T', 'B'],
#                                                   'text is')]
ds = DocumentSummarizer()

def glueCommunicator():
    # better create tokenizer object here
    state = "stop"
    id = 0
    while content_queue:
        # check for start token
        if content_queue[0] == 1:
            content_queue.popleft()
            state = "start"
            id = int(content_queue[0][0])
	    # push doc id
            summarize_queue.append(id)
        elif content_queue[0] == 0:
            content_queue.popleft()
            state = "end"

        if state == "start":
            docId, fields, text = content_queue.popleft()
            ptoken = tokenize(text)
            tmp = (fields, ptoken)
            summarize_queue.append(tmp)
            # print "Doc ID: %s Fields: %s" % (docId, fields)
            # print text
            # processed tokens list
            # ptokens = tk.tokenize(text)
        else:
            # start tokenizer on a single doc contents
	    # push doc id as end token
            summarize_queue.append(id)

def connectToSummarizer():
    state = "stop"
    seenId = 0
    docid = 0
    doc_queue = deque()
    while summarize_queue:
	# check for start token
	if not seenId and isinstance(summarize_queue[0], (int, long)):
	    docid = summarize_queue.popleft()
	    state = "start"
	    seenId = 1
	elif seenId and docid == summarize_queue[0]:
	    summarize_queue.popleft()
	    state = "end"
	    seenId = 0
	if state == "start":
	    doc_queue.append(summarize_queue.popleft())
	else:
	    # start summarizer on a single doc content
	    ds.summarize(docid, doc_queue)
	    doc_queue.clear()	
