import os, requests
import threading
import urllib.request as urllib2
import time
import os
from sys import stdout

URL = rf'https://downloads.arduino.cc/arduino-1.8.19-windows.exe'

def _restart_line():
    stdout.write('\r')
    stdout.flush()

def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst

def main(url=None, splitBy=3):
    start_time = time.time()
    if not url:
        print ("Please Enter some url to begin download.")
        return

    fileName = url.split('/')[-1]
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    print ("%s bytes to download." % sizeInBytes)
    if not sizeInBytes:
        print ("Size cannot be determined.")
        return

    dataDict = {}
    loding = {}

    # split total num bytes into ranges
    ranges = buildRange(int(sizeInBytes), splitBy)

    def downloadChunk(idx, irange):
        total = b""
        req = urllib2.Request(url)
        req.headers['Range'] = 'bytes={}'.format(irange)
        #  = urllib2.urlopen(req).read()
        u = urllib2.urlopen(req)
        meta = u.info()
        file_size = int(meta.get("Content-Length"))
        print(f"file size {file_size/1000000}MB")
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            downloading = int(file_size_dl * 100 / file_size)*'='
            status = f"download{idx} {(file_size_dl/1000000):.2f}MB - {downloading}> ,{(file_size_dl * 100 / file_size):.2f}% {file_size/1000000}MB"
            # status = status + chr(8)*(len(status)+1)
            total = total+buffer
            loding[idx] = status
            print('---------------------------------------------------------')
            for i in loding:
                print(loding[i])
                
            # stdout.write(status)
            # stdout.flush()
            # _restart_line()
        dataDict[idx] = total
        
        
        
    # create one downloading thread per chunk
    downloaders = [
        threading.Thread(
            target=downloadChunk, 
            args=(idx, irange),
        )
        for idx,irange in enumerate(ranges)
        ]

    # start threads, let run in parallel, wait for all to finish
    for n , th in enumerate(downloaders):
        th.start()
    for th in downloaders:
        th.join()
        
    print (f'done: got {len(dataDict)} chunks, total {sum( len(chunk) for chunk in dataDict.values())} bytes')

    print ("--- %s seconds ---" % str((time.time() - start_time)/60))

    if os.path.exists(fileName):
        os.remove(fileName)
    # reassemble file in correct order
    with open(fileName, '+wb') as fh:
        for _idx,chunk in sorted(dataDict.items()):
            fh.write(chunk)

    print ("Finished Writing file %s" % fileName)
    print ('file size {} bytes'.format(os.path.getsize(fileName)*1000))

if __name__ == '__main__':
    main(URL)
