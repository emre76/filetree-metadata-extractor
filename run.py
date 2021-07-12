import sys
import os
import time
from filetreemetadataextractor import FiletreeMetadataExtractor
import urllib.request, json

def main():
    if len(sys.argv)-1 == 2:
    #there must be two user arguments
        print("file to download from:\n", sys.argv[1])
        print ("the output file name should be:\n", sys.argv[2])
    else:
        raise BaseException("Call only with two arguments: the path of the input file and output file name")
    '''
    create a directory under /files for:
        download of input data 
        saving of output data
'''

    #create a unique directory with a name marked with  create date in millisec
    if not os.path.exists('files'):
        os.mkdir("files")
    dir_name = "files/" + str(int(time.time()*1000))
    os.mkdir(dir_name)

    #read the data from the cli 1.argument and save it in parallel
    with urllib.request.urlopen(sys.argv[1]) as url:
        read = url.read()
        readdecode = read.decode()
        with open(dir_name+'/'+'input.json', 'b+w') as f:
                f.write(read)
        data = json.loads(readdecode)

    #instantiate an object with read input data and the name of the output data
    metadataObject = FiletreeMetadataExtractor(data, dir_name+'/'+sys.argv[2])
    #parse the data and generate output data
    metadataObject.parseRows()

if __name__ == '__main__':
    # protects users from accidentally invoking
    main()
