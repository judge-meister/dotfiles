#!/usr/bin/env python3

import os
import sys
import getopt
import logging
import glob
from subprocess import getstatusoutput as unix

def usage():
    """"""
    print("Usage: mkthumbs.py <dir dir ...>")
    print(" -q quiet")
    print(" -p progress")
    print(" -n dryrun")
    print(" -r recurse")
    print(" -R repeat or recreate")
    print(" -s scale (no implemented!)")
    print(" -t file type (jpg or png:default)")
    print(" -d print debug info")

def getOptions():
    """"""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hqpnrdRt:s:", 
        ["help", "quiet", "progress", "debug", "recurse", "repeat", "type=", "scale"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    options = {}
    options['quiet'] = False
    options['progress'] = False
    options['recurse'] = False
    options['recreate'] = False
    options['dryrun'] = False
    options['debug'] = False
    options['type'] = '.png'
    options['scale'] = False
    
    for o, a in opts:
        if o == "-q":
            options['quiet'] = True
        elif o == "-p":
            options['progress'] = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-t", "--type"): # thumbnail file extention
            if a in ('png', 'jpg'):
                options['type'] = '.'+a
            else:
                print("ERROR: Invalid type specified - png or jpg only (got %s)" % a)
                sys.exit()
        elif o in ("-r", "--recurse"):
            options['recurse'] = True
        elif o in ("-R", "--recreate"):
            options['recreate'] = True
        elif o in ("-n", "--dryrun"):
            options['dryrun'] = True
        elif o in ("-d", "--debug"):
            options['debug'] = True
        elif o in ("-s", "--scale"):
            options['scale'] = True
        else:
            assert False, "unhandled option"

    #print("ARGS",args)
    options['dirs'] = []
    if len(args) > 0:
        for a in args:
            if os.path.isdir(a) and a.find('.pics') == -1:
                options['dirs'].append(a)
            else:
                print(f"ERROR: {a} is not a valid directory.")
                sys.exit()
    else:
        options['dirs'].append('.')
        
    return options

    
class MkThumbs:
    def __init__(self, options):
        """"""
        self.dirs = options['dirs']
        self.options = options
        self.picsdir = '.pics'
        #self.meddir = '.med'
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")

    def progress(self, str='.'):
        """"""
        sys.stdout.write(str)
        sys.stdout.flush()

    def createThumb(self, image, thumb):
        """"""
        cmd = f"convert -define jpeg:size=500x500 \"{image}\"  -auto-orient -thumbnail 240x240 -unsharp 0x.5 \"{thumb}\" "
        if self.options['dryrun']:
            self.debug(cmd)
        else:
            status, output = unix(cmd)
            #logging.info(f"{image}")
            if status != 0:
                print(f"{status} {output}")

    def createGifThumb(self, image, thumb):
        """"""
        cmd = f"convert -define jpeg:size=500x500 \"{image}[0]\"  -auto-orient -thumbnail 240x240 -unsharp 0x.5 \"{thumb}\" "
        if self.options['dryrun']:
            self.debug(cmd)
        else:
            status, output = unix(cmd)
            #logging.info(f"{image}")
            if status != 0:
                print(f"{status} {output}")


    #def scaleImage(self, image, thumb):
    #    """"""
    #    cmd = f"convert -define jpeg:size=4000x4000 {image}  -auto-orient -thumbnail 3840x3840 -unsharp 0x.5 {thumb}"
    #    if self.options['dryrun']:
    #        self.debug(cmd)
    #    else:
    #        status, output = unix(cmd)
    #        logging.info(f"{image}")
    #        if status != 0:
    #            print(f"{status} {output}")
        
    #def isImageLarge(self, name):
    #    """"""
    #    cmd = f"identify {name} | cut -d' ' -f3"
    #    if self.options['dryrun']:
    #        self.debug(cmd)
    #    else:
    #        status, output = unix(cmd)
    #        #logging.info(f"{image}")
    #        if status != 0:
    #            print(f"{status} {output}")
    #        w,h = output.split('x')
    #        if int(w) > 3840 or int(h) > 3840:
    #            self.scaleImage(name, self.getScaledName(name))

    def getThumbName(self, name):
        """"""
        return os.path.join(os.path.dirname(name), self.picsdir, os.path.basename(os.path.splitext(name)[0])+self.options['type'])

    #def getScaledName(self, name):
    #    """"""
    #    return os.path.join(os.path.dirname(name), self.meddir, os.path.basename(os.path.splitext(name)[0])+'.jpg')
        
    def doFolder(self, folder):
        """"""
        self.debug("doFolder")
        if not os.path.exists(os.path.join(folder, self.picsdir)):
            os.makedirs(os.path.join(folder, self.picsdir))
        #if not os.path.exists(os.path.join(folder, self.meddir)):
        #    os.makedirs(os.path.join(folder, self.meddir))
        #print("glob",glob(f"{folder}/*.jpg"))
        image_list = glob.glob(glob.escape(f"{folder}")+"/*.jpg") + glob.glob(glob.escape(f"{folder}")+"/*.jpeg") + glob.glob(glob.escape(f"{folder}")+"/*.png") + glob.glob(glob.escape(f"{folder}")+"/*.gif") 
        image_list.sort()
        print(f"{folder} - {len(image_list)}")
        progend=''
        for fn in image_list:
            if not os.path.exists(self.getThumbName(fn)) or self.options['recreate']:
                if os.path.splitext(fn)[1] == ".gif":
                    self.createGifThumb(fn, self.getThumbName(fn))
                else:
                    self.createThumb(fn, self.getThumbName(fn))
                progend='\n'
                self.progress()
        self.progress(progend)
        #for fn in image_list:
        #    if not os.path.exists(self.getScaledName(fn)) or self.options['recreate']:
        #        self.scaleImage(fn, self.getScaledName(fn))
            
    def doTree(self, folder):
        """"""
        self.debug("doTree")
        for root, dirs, files in os.walk(folder):
            if os.path.basename(root) not in ['.pics']:
                self.debug(f"{root}")
                self.doFolder(root)
                    
    def process(self):
        """"""
        for dirn in self.dirs:
            if self.options['recurse']:
                self.doTree(dirn)
            else:
                self.doFolder(dirn)
        
    def debug(self, str):
        """"""
        if self.options['debug']:
            print(f"DEBUG: {str}")
    
def main():
    """"""
    options = getOptions()
    
    mkthumbs = MkThumbs(options)
    mkthumbs.process()
        
    
if __name__ == "__main__":
    main()
