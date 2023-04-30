#!/usr/bin/python3
#set -x

import sys, os, glob
from subprocess import getstatusoutput as unix

MAX=5670
   
def progress(str='.'):
    """"""
    sys.stdout.write(str)
    sys.stdout.flush()
    

def main():
    if len(sys.argv) == 1: #if [ "$1" == "" ]
        print("Provide a dir name even if it is .")
        sys.exit()

    for dirn in sys.argv[1:]:
        CWD = os.getcwd()
        os.chdir(dirn)

        jpegs = glob.glob('*.jpg')
        print(f"{dirn} - {len(jpegs)}")
        progend = ""
        for x in jpegs:
            #print(f"identify \"{x}\" | cut -d' ' -f3")
            ret, wh = unix(f"identify \"{x}\" | cut -d' ' -f3")
            #print(f"{ret}, {wh}")
            w,h = wh.split('x')
            w = int(w)
            h = int(h)

            if w > MAX or h > MAX:
                if not os.path.exists(".orig"): 
                    os.makedirs(".orig")
                if not os.path.exists(f".orig/{x}"):
                    os.rename(x, f".orig/{x}") #/bin/mv -f "$x" ".orig/$x"
                    #print(f"scaling {x}")
                    progress()
                    progend = "\n"
                    #convert -define jpeg:size=${MAX}x${MAX} ".orig/$x"  -auto-orient -thumbnail ${MAX}x${MAX} -unsharp 0x.5 "$x"
                    ret, out = unix(f"convert \".orig/{x}\"  -auto-orient -thumbnail {MAX}x{MAX} -unsharp 0x.5 \"{x}\" ")
        os.chdir(CWD)
        progress(progend)


#  convert -define jpeg:size=4000x4000 {image}  -auto-orient -thumbnail 3840x3840 -unsharp 0x.5 {thumb}

if __name__ == '__main__':
    main()

