from itertools import imap
from operator import itemgetter
import heapq
import os


def extract_termid(line):
    """Extract termid and convert to a form that gives the
       expected result in a comparison
    """
    return line.split()[0]  # for example


def merge_sortedfiles(file1, file2, i):
    with open(file1) as f1, open(file2) as f2:
        sources = [f1, f2]
        with open("./indexes/layer8/merged"+str(i)+".txt", "w") as dest:
            decorated = [((extract_termid(line), line) for line in f)
                                                        for f in sources]

            merged = heapq.merge(*decorated)
            undecorated = imap(itemgetter(-1), merged)
            dest.writelines(undecorated)


if __name__ == '__main__':
    #files = os.listdir('./indexes/')[:278]
    files = os.listdir('./indexes/layer7')
    # files.remove('120mb')
    # files.remove('layer1')
    print "merge started..."
    #basepath = "./indexes/"
    basepath = "./indexes/layer7/"
    i = 0
    while files:
        file1 = basepath + files.pop(0)
        file2 = basepath + files.pop(0)
        merge_sortedfiles(file1, file2, i)
        i += 1
    print "merge ended"





#file1 = "../indexes/out0.txt"
#file2 = "../indexes/out1.txt"
#merge_sortedfiles(file1, file2)


