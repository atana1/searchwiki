# reads index and makes dictionary


def readindex(rserver, indexfile):
    """ reads the index file and builds
        inverted index
    """
    with open(indexfile, 'r') as f:
        # print "started"
        previd = str(0)
        termid = str(0)
        docid = 0
        terminfo = {}
        terminfo['docid'] = []
        for line in f:
            # print "in"
            line = line.split(":")
            termid = line.pop(0)
            # print "previd: ", previd
            # print "termid: ", termid
            if previd != termid:
                # means next termid
                # print "doclist: ", terminfo['docid']
                map = {'df': len(terminfo['docid']), 'doclist': 'd'+str(previd)}
                rserver.hmset(previd, map)
                # dict creation
                for el in terminfo['docid']:
                    # key: docid; value: (fcount, fdict)
                    value = (el['count'], el['fd'])
                    map = {el['id']: value}
                    rserver.hmset('d'+str(previd), map)
                terminfo.clear()
                terminfo['docid'] = []
            # format is like "0:5:C1:B1"
            # line = line.split(":")
            # termid = line.pop(0)

            docid = line.pop(0)
            fdict = {}
            totalfcount = 0
            for elem in line:
                field = elem[0]
                fcount = int(elem[1:])
                fdict[field] = fcount
                totalfcount += fcount
            # finished processing a line
            terminfo['id'] = termid
            terminfo['docid'].append({'id': docid, 'count': totalfcount,
                                      'fd': fdict})
            previd = termid
        # end of file; write things for last line
        # print "EOF"
        # print "doc list", terminfo['docid']
        map = {'df': len(terminfo['docid']), 'doclist': 'd'+str(previd)}
        rserver.hmset(previd, map)
        # dict creation
        # print "doc list:", terminfo['docid']
        for el in terminfo['docid']:
            value = (el['count'], el['fd'])
            map = {el['id']: value}
            # print map
            rserver.hmset('d'+str(previd), map)
        terminfo['docid'] = []
        terminfo.clear()
    f.close()


def readtitlemapping(rserver, titlemapfile):
    """ reads document id to title map
    """
    with open(titlemapfile, 'r') as f:
        count = 1
        for line in f:
            # read for only k documents
            if count == 6000:
                break
            docid, title = line.split("=")[:2]
            map = {docid: title}
            rserver.hmset("docidTotitle", map)
            count += 1
    f.close()


def readwordtoidmapping(rserver, filepath):
    """ reads word to word id mapping
    """
    with open(filepath, 'r') as f:
        for line in f:
            temp = line.split(" ")
            word = temp[0]
            id = temp[1].split("\n")[0]
            map = {word: id}
            rserver.hmset("wordToId", map)
    f.close()
# readindex(rserver, 'scratch/index.txt')
