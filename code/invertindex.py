from utils import bags


def create_invertedIndexB(filename):
    """ creates inverted index for a block
        and writes to a intermediate file
    """
    # sort based on term id
    if bags:
        bags.sort(key=lambda x: x[0])
        basedir = 'indexes/'
        with open(basedir+filename, "wa") as f:
            while bags:
                item = bags.pop(0)
                f.write(str(item[0]) + " " + str(item[1]) + item[2] + "\n")
            f.close()
        print "%s created" % (filename)

def invertedIndexHandler(index):
    prefix = "out"
    suffix = ".txt"

    # check if bag not empty
    if not bags:
        print "No summary token in bags!"
        return

    filename = prefix + str(index) + suffix
    create_invertedIndexB(filename)
