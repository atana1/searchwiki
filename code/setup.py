from readindex import readindex, readtitlemapping, readwordtoidmapping
import time
import redis


rserver = redis.Redis("localhost")


if __name__ == '__main__':
    print "setting up the search engine..."
    indexfile = "indexes/in.txt"
    titlemapfile = 'mapping/title_map.txt'
    filepath = 'mapping/word-id-map.txt'
    print "building inverted index.."
    t = time.time()
    #readindex(rserver, indexfile)
    print "inverted index contruction completed in %s secs" % (time.time()-t)
    print "building document id --> title mapping..."
    t = time.time()
    #readtitlemapping(rserver, titlemapfile)
    print "mapping finished in %s secs" % (time.time()-t)
    print "building word to word id mapping..."
    t = time.time()
    readwordtoidmapping(rserver, filepath)
    print "finished building word to word id mapping in %s secs" %(time.time()-t)
    print "setup complete."
    rserver.shutdown()
