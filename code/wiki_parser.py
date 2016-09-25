import xml.sax
import sys
import time
from conf import MAXDOCLIMIT
from invertindex import invertedIndexHandler
#from tokenizer import Tokenizer
from utils import content_queue, summarize_queue, bags, WordLexicon
# from collections import namedtuple
#from intermediator import glueCommunicator
from binder import glueCommunicator, connectToSummarizer


# DocLexicon = {}
# care in setting maximum limit(total documents in future
# can be more than this value)
# MAX = 100000
# CheckWords = {">": 1, "<" : 1, '"': 1, ",": 1,
#              "/ref": 1, "\n": 1}
NOISELEN = 5
START = 1
END = 0
ON = 1
OFF = 0
#t = Tokenizer()
#Fields = namedtuple('Field', 'T B I C L R')


class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.doc_count = 0
        self.curr_tag = ""
        self.outFileIndex = 0
        # ['R', 'L', 'C', 'I']
        self.fIndicator = [OFF, OFF, OFF, OFF]
        self.docId = []
        self.title = ""
        self.text = ""
        self.category = ""
        self.links = ""
        self.ref = ""
        self.infobox = ""

    def startElement(self, tag, attr):
        self.curr_tag = tag
        if tag == "page":
            # At the begining of document push start token
            content_queue.append(START)

    def endElement(self, tag):
        # print "Current tag: ", self.curr_tag
        # doesn't detect end of page tag.
        # yeah, that's weird :P
        # if self.curr_tag == "page":
            # write title to content queue
            # content_queue.append((self.docId, self.title))
            # print "in here"
            # print "Title: ", self.title
            # self.title = ""
            # self.docId = 0
        if self.curr_tag == "text":
            # treating this as end of document
            # print "Doc ID : %s Title : %s" % (self.docId[0], self.title)
            docId = self.docId[0]
            content_queue.append((docId, ['T'], self.title))
            # push end token
            content_queue.append(END)
            self.fIndicator = [OFF, OFF, OFF, OFF]
            self.title = ""
            self.docId = []
            self.doc_count += 1
        # process title after text
        # (id occurs before title)
        # elif self.curr_tag == "text":
            # text_cont = "".join(self.text)
            # print "Doc ID : ", self.docId
            # print text_cont
            # print "*******************"
            # do we need to delete memory
            # self.text = []
        if self.doc_count == MAXDOCLIMIT:
            print "%s document parsed" % (MAXDOCLIMIT)
            print "started normalization.."
            # tokenize
            glueCommunicator()
            print "normalization complete"
            # summarize
            print "started summarization"
            connectToSummarizer()
            print "summarization complete"
            # make intermediate inverted index for the block
            print "building inverted index %s..." %(self.outFileIndex)
            invertedIndexHandler(self.outFileIndex)
            print "inverted index created"
            self.outFileIndex += 1
            # reset doc count
            self.doc_count = 0

        self.curr_tag = ""

    def characters(self, content):
        # set document id
        if self.curr_tag == "id":
            id = int(content)
            # if id < MAX:
                #self.docId = id
            self.docId.append(id)
        elif self.curr_tag == "title":
            # handle title
            # print "Title - ", content.encode('utf-8')
            self.title = content.encode('utf-8')
            # print self.title
        elif self.curr_tag == "text":
            # print "Text - ", content.encode('utf-8')
            # text comes line by line
            docText = content.encode('utf-8')
            # print docText
            docId = self.docId[0]
            # self.text.append(content.encode('utf-8'))
            # Handle references, links and others
            if docText.startswith("}}") or len(docText) > NOISELEN:
                # print docText
                # handle references
                if docText.startswith("== Ref") or docText.startswith("==Ref"):
                    self.fIndicator[0] = ON
                    if self.fIndicator[1]:
                        self.fIndicator[1] = OFF
                elif docText.startswith("== Ext") or docText.startswith("==Ext"):
                    self.fIndicator[1] = ON
                    if self.fIndicator[0]:
                       self.fIndicator[0] = OFF
                elif docText.startswith("{{Inf"):
                    self.fIndicator[3] = ON
                elif docText.startswith("[[Cat"):
                    self.fIndicator[2] = ON
                elif docText.startswith("}}") and self.fIndicator[3]:
                    self.fIndicator[3] = OFF
                elif docText.startswith("=="):
                    if self.fIndicator[0]:
                        self.fIndicator[0] = OFF
                    if self.fIndicator[1]:
                        self.fIndicator[1] = OFF

                # check on field
                setField = []
                ind = self.fIndicator
                if ind[0]:
                    setField.append('R')
                if ind[1]:
                    setField.append('L')
                if ind[3]:
                    setField.append('I')
                if ind[2]:
                    setField.append('C')
                setField.append('B')
                fields = setField[:]

                # print "DocID: %s Fields: %s" %(docId, fields)
                # print docText
                content_queue.append((docId, fields, docText))
                if ind[2]:
                    ind[2] = OFF
                #ptok = t.tokenize(docText)
                #print "******"
                #print "Doc ID: ", self.docId
                #print ptok


if __name__ == '__main__':
    wiki_dump, index_path = sys.argv[1:]
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wh = WikiHandler()
    parser.setContentHandler(wh)
    t = time.time()
    parser.parse(open(wiki_dump, "r"))
    # print "Title"
    # print wh.title
    # print "----------text---------------"
    # print wh.text[0:10]
    # print content_queue
    glueCommunicator()
    print time.time()-t
    t = time.time()
    connectToSummarizer()
    bags.sort(key=lambda x: x[0])
    f = open(index_path, "wa")

    prevdocId = 0
    for item in bags:
        docId = item[1]
        diff = docId - prevdocId
        # writing words instead of wordID
        #f.write(item[0].encode('utf-8')+" "+str(item[1])+str(item[2])+"\n")
        f.write(str(item[0])+" "+str(diff)+ item[2] +"\n")
        prevdocId = docId

    print time.time()-t
    #print summarize_queue
    #content_queue.clear()
