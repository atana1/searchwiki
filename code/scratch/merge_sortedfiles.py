from itertools import imap
from operator import itemgetter
import heapq
import os


def extract_termid(line):
    """Extract termid and convert to a form that gives the
       expected result in a comparison
    """
    return line.split()[0]  # for example


def merge_sortedfiles(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        sources = [f1, f2]
        with open("./indexes/layer1/merged.txt", "w") as dest:
            decorated = [((extract_termid(line), line) for line in f)
                                                        for f in sources]

            merged = heapq.merge(*decorated)
            undecorated = imap(itemgetter(-1), merged)
            dest.writelines(undecorated)


if __name__ == '__main__':
    files = os.listdir('./indexes/')[:270]
    print "merge started..."
    while files:
        file1 = files.pop(0)
        file2 = files.pop(0)
        merge_sortedfiles(file1, file2)
    print "merge ended"





#file1 = "../indexes/out0.txt"
#file2 = "../indexes/out1.txt"
#merge_sortedfiles(file1, file2)


