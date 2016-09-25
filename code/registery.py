import sys
import time
import xml.sax


import binder
import invertindex
from utils import content_queue


from wiki_parser import WikiHandler


def start_registary(wiki_dump):
    """ registary for parsing wiki dump and
        creating intermediate inverted indexes
    """
    index = 0
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wh = WikiHandler()
    parser.setContentHandler(wh)
    with open(wiki_dump, "r") as f:
        print "started parsing..."
        parser.parse(f)
        index = wh.outFileIndex
        f.close()

    # if content queue is not empty then make inverted index
    # for that block
    if content_queue:
        binder.glueCommunicator()
        binder.connectToSummarizer()
        invertindex.invertedIndexHandler(index)


if __name__ == "__main__":
    wiki_dump = sys.argv[1]
    print "=================process started===================="
    t = time.time()
    start_registary(wiki_dump)
    print time.time() - t
    print "intermediate inverted index creation complete.."
