

def change_format(filepath, destpath):
    with open(filepath, 'r') as f, open(destpath, 'w') as dest:
        for line in f:
            char = []
            for ch in line:
                if ch != '\n' and (ch == " " or not (48 <= ord(ch) <= 58)):
                    char.append(":")
                    if ch != " ":
                        char.append(ch)
                else:
                    char.append(ch)
            # write to destination file
            text = "".join(char)
            dest.write(text)


if __name__ == '__main__':
    sourcefile = "merged0.txt"
    destfile = "indexfinal.txt"
    change_format(sourcefile, destfile)

