# https://www.codingame.com/ide/puzzle/mime-type
dictionary = {}
n = int(raw_input())  # Number of elements which make up the association table.
q = int(raw_input())  # Number Q of file names to be analyzed.
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = raw_input().split()
    dictionary[ext.lower()] = mt
for i in range(q):
    fname = raw_input()  # One file name per line.
    farr = fname.split('.')
    if len(farr)>1:
        try:
            print(dictionary[farr[-1].lower()])
        except KeyError:
            print("UNKNOWN")
        except IndexError:
            print("UNKNOWN")
    else:
        print("UNKNOWN")
# For each of the Q filenames, display on a line the corresponding MIME type. If there is no corresponding type, then display UNKNOWN.



