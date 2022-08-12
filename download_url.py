import requests
import urllib3
from sys import stdout
from urllib.request import urlopen
import progressbar
import time

def _restart_line():
    stdout.write('\r')
    stdout.flush()

def download(url):
    widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('*'),' (',
           progressbar.ETA(), ') ',
          ]
  
    bar = progressbar.ProgressBar(max_value=100, 
                              widgets=widgets).start()
    
    file_name = url.split('/')[-1]
    u = urlopen(url)
    print(u)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.get("Content-Length"))
    print(f"Downloading: {file_name} MB: {file_size/1000}")

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        # downloading = int(file_size_dl * 10 / file_size)*'='
        # status = f"download {(file_size_dl/1000000):.2f} - {downloading}> ,{(file_size_dl * 100 / file_size):.2f} %"
        bar.update(int(file_size_dl * 100 / file_size))
        # status = status + chr(8)*(len(status)+1)
        # stdout.write(status)
        # stdout.flush()
        # _restart_line()

    f.close()
    
def main():
    for i in range(6,7):
        url = f'https://raw.githubusercontent.com/SuperTux/supertux/master/data/images/creatures/tux/small/grow-{i}.png'
        url = rf'https://downloads.arduino.cc/arduino-1.8.19-windows.exe'
        download(url)
    
main()