#!/usr/bin/env python3
"""
#
# Create a Montage Wallpaper
#
# assumption is wallpaper will be 1920x1200
#
# max images across is 5 portrait
# min images across is 2 landscape + 1 portrait
# 2 rows of these fit on the wallpaper
#
# start by randomly selecting some images
# work out if they fit the criteria above
#
# normalize the aspect/dimensions so that 2 portrait images will fit is same space as 1 landscape
#  - 16x10 screen as 1920x1200 resolution means each image portrait should be resized to 384x600
#    and each landscape image should be resized to 768x600
#  - 1920/5 x 1200/2 (384x600) and 1920/2.5 x 1200/2 (768/600)
#  - 1366/5 x 768/2 (273/384) and 1366/2.5 x 768/2 (546x384)

# create each row and then combine the rows into one final image
#
"""
# Requires: feh

# pylint: disable=invalid-name

#redefined-outer-name

import os
import sys
import getopt
from random import random
from glob import glob
from subprocess import getstatusoutput as unix
from PIL import Image

Verbose = False
# montage options
CONCAT = " -mode Concatenate"
BLACK = " -background black"


def verbose_print(msg):
    """verbose logging"""
    #global Verbose
    if Verbose:
        print(msg)


def enough_files(filelist, layout):
    """check if there is enough files and enough variety in portrait and landscape"""
    print("enough_files()")
    pc, lc = 0, 0
    lw, lh = layout

    #for i in range(len(filelist)):
    for img in filelist:
        port = True
        #img = filelist[i]

        w, h = Image.open(img).size
        if w > h:
            port = False

        if port:
            verbose_print("Portrait")
            pc += 1
        else:
            verbose_print("Landscape")
            lc += 1
    rc = pc + 2*lc

    verbose_print(f"pc = {pc}, lc = {lc}, rc = {rc} (wxh = {lw*lh})") # % (pc, lc, rc, lw*lh))

    # if w is odd then min 2x port
    # total count >= w*h
    if rc < lw*lh:
        verbose_print("ERROR: not enough images")
        return False
    if (lw % 2 != 0 and pc < 2):
        verbose_print("ERROR: not enough portrait images")
        return False

    return True


def create_layout(filelist, layout):
    """collect the files for the montage wallpaper """
    print("create_layout()")
    row = {}
    all_imgs = []
    montage = []
    rc = 0
    rw = 0
    pc = 0
    lc = 0

    Done = False
    #for i in range(len(filelist)):
    while not Done:
        r = int(random()*len(filelist))
        img = filelist[r]

        # elliminate duplicates
        if img in all_imgs or img.find('montage') > -1:
            continue

        # determine if landscape or portrait
        # assume portrait to start
        port = True
        w, h = Image.open(img).size
        if w > h:
            port = False

        if port:
            verbose_print("Portrait")
            pc += 1
        else:
            verbose_print("Landscape")
            lc += 1

        # if portrait and remaining width >= 1 then add, else if land and remaining >= 2 the add
        if port and (layout[0]-rw) >= 1:
            #row.append((img, port))
            row[rc] = {'name':img, 'port':port, 'w':w, 'h':h}
            all_imgs.append(img)
            rc += 1
            rw += 1
        elif not port and (layout[0]-rw) >= 2:
            #row.append((img, port))
            row[rc] = {'name':img, 'port':port, 'w':w, 'h':h}
            all_imgs.append(img)
            rc += 1
            rw += 2

        #print(row)
        # once we have a row width of 5 add the row to montage layout
        if rw == layout[0] and len(montage) == 1:
            montage.append(row)
            # now we have 2 rows exit the loop
            #break
            Done = True
        elif rw == layout[0]:
            montage.append(row)
            rw = 0
            rc = 0
            row = {}

    return montage


def print_layout(montage):
    """display a guide to the layout of this montage"""
    for row in montage:
        for i in row:
            if row[i]['port']: #port:
                print("[]",end='')
            else:
                print("[  ]",end='')
        print("")


def build_row(row, i):
    """create a single row montage"""
    print(f"build_row({i})")

    files = ' '.join([row[x]['name'] for x in row])
    mont_img = f"mont{i}.png"
    #os.system('montage -tile x1 -geometry 600x600 %s %s' % (files, mont_img))
    cmd = f"montage -quiet {files} {BLACK} {CONCAT} -tile x1 -geometry +0+0 {mont_img}" \
        #  % (files, mont_img)
    verbose_print(cmd)
    os.system(cmd)
    return mont_img


def combine_rows(one, two, dims):
    """montage the 2 rows together"""
    print("combine_rows()")
    pid = os.getpid()
    cmd = f"montage {one} {two} {BLACK} {CONCAT} -tile x2 -geometry +0+0 tmp{pid}.png"
            # % (one, two, pid)
    verbose_print(cmd)
    os.system(cmd)
    #cmd0 = 'convert tmp%d.png -size %dx%d -stroke black -strokewidth 4 -draw "line 0,0 %d,0" ' \
    #      '-draw "line %d,0 %d,%d" -draw "line %d,%d 0,%d" -draw "line 0,%d 0,0" ' \
    #      'montage_%s_%d.jpg' % (pid, dims['sw'], dims['sh'], dims['sw']-1, dims['sw']-1, \
    #      dims['sw']-1, dims['sh']-1, dims['sw']-1, dims['sh']-1, dims['sh']-1, dims['sh']-1, \
    #      dims['size'], pid)
    cmd = f"convert tmp{pid}.png -size {dims['sw']}x{dims['sh']} -stroke black -strokewidth 4 " \
          f"-draw \"line 0,0 {dims['sw']-1},0\" " \
          f"-draw \"line {dims['sw']-1},0 {dims['sw']-1},{dims['sh']-1}\" " \
          f"-draw \"line {dims['sw']-1},{dims['sh']-1} 0,{dims['sh']-1}\" " \
          f"-draw \"line 0,{dims['sh']-1} 0,0\" " \
          f"montage_{dims['size']}_{pid}.jpg"
    #if cmd0 != cmd:
    #    print("f-string conversion failed (line 192)")
    #    print(cmd0)
    #    print(cmd)
    #    sys.exit()
    verbose_print(cmd)
    os.system(cmd)
    name = f"montage_{dims['size']}_{pid}.jpg" #% (dims['size'], pid)
    print(name)
    return name


def normalize_image(img, norm, dims):
    """use convert to reshape the image into norm filename adding a black border"""
    # convert -crop wxh+off+0
    verbose_print("normalise_image()")
    tmp = f"tmp{os.getpid()}.png"

    print("normalise:",img['name'])
    if img['port']:
        verbose_print("resize from wxh to 384x600 (cropping excess with, keeping it centred)")
        off = (img['w']-((img['h']/dims['ph'])*dims['pw']))/2
        verbose_print(f"off {off} = ({img['w']} - (({img['h']} / {dims['ph']}) * ' \
                      '{dims['pw']})) / 2")
            # % (off, img['w'], img['h'], dims['ph'], dims['pw']))
        cmd = f"convert -crop {img['w']-(2*off)}x{img['h']}+{off}+0 \"{img['name']}\" \"{tmp}\""
            # % (img['w']-(2*off), img['h'], off, img['name'], tmp)
        verbose_print(cmd)
        os.system(cmd)
        verbose_print("add black borders")
        #cmd0 = 'convert -quiet -quality 100 -size %dx%d -resize %dx%d -stroke black ' \
        #      '-strokewidth 3 -draw "line 0,0 %d,0" -draw "line %d,0 %d,%d" ' \
        #      '-draw "line %d,%d 0,%d" -draw "line 0,%d 0,0" "%s" "%s"' % (dims['pw'], \
        #      dims['ph'], dims['pw'], dims['ph'], dims['pw']-1, dims['pw']-1, dims['pw']-1, \
        #      dims['ph']-1, dims['pw']-1, dims['ph']-1, dims['ph']-1, dims['ph']-1, tmp, norm)
        cmd = f"convert -quiet -quality 100 -size {dims['pw']:.0f}x{dims['ph']:.0f} " \
              f"-resize {dims['pw']:.0f}x{dims['ph']:.0f} -stroke black -strokewidth 3 " \
              f"-draw \"line 0,0 {dims['pw']-1:.0f},0\" " \
              f"-draw \"line {dims['pw']-1:.0f},0 {dims['pw']-1:.0f},{dims['ph']-1:.0f}\" " \
              f"-draw \"line {dims['pw']-1:.0f},{dims['ph']-1:.0f} 0,{dims['ph']-1:.0f}\" " \
              f"-draw \"line 0,{dims['ph']-1:.0f} 0,0\" \"{tmp}\" \"{norm}\""
        #if cmd0 != cmd:
        #    print("f-string conversion failed (line 223)")
        #    print(cmd0)
        #    print(cmd)
        #    sys.exit()
        verbose_print(cmd)
        os.system(cmd)
    else:
        verbose_print("resize to 768x600")
        off = (img['w']-((img['h']/dims['lh'])*dims['lw']))/2
        verbose_print(f'off {off} = ({img["w"]} - (({img["h"]} / {dims["lh"]}) * {dims["lw"]})) /2')
        cmd = f"convert -crop {img['w']-(2*off)}x{img['h']}+{off}+0 \"{img['name']}\" \"{tmp}\""
        verbose_print(cmd)
        os.system(cmd)
        verbose_print("add black borders")
        #cmd0 = 'convert -quiet -quality 100 -size %dx%d -resize %dx%d -stroke black ' \
        #      '-strokewidth 3 -draw "line 0,0 %d,0" -draw "line %d,0 %d,%d" ' \
        #      '-draw "line %d,%d 0,%d" -draw "line 0,%d 0,0" "%s" "%s"' \
        #      % (dims['lw'], dims['lh'], dims['lw'], dims['lh'], dims['lw']-1, dims['lw']-1,
        #      dims['lw']-1, dims['lh']-1, dims['lw']-1, dims['lh']-1, dims['lh']-1, dims['lh']-1,
        #      tmp, norm)
        cmd = f"convert -quiet -quality 100 -size {dims['lw']:.0f}x{dims['lh']:.0f} " \
              f"-resize {dims['lw']:.0f}x{dims['lh']:.0f} -stroke black -strokewidth 3 " \
              f"-draw \"line 0,0 {dims['lw']-1:.0f},0\" " \
              f"-draw \"line {dims['lw']-1:.0f},0 {dims['lw']-1:.0f},{dims['lh']-1:.0f}\" " \
              f"-draw \"line {dims['lw']-1:.0f},{dims['lh']-1:.0f} 0,{dims['lh']-1:.0f}\" " \
              f"-draw \"line 0,{dims['lh']-1:.0f} 0,0\" \"{tmp}\" \"{norm}\""
        #if cmd0 != cmd:
        #    print("f-string conversion failed (line 250)")
        #    print(cmd0)
        #    print(cmd)
        #    sys.exit()
        verbose_print(cmd)
        os.system(cmd)


def build_montage(montage, dims):
    """build the montage in stages"""
    one = build_row(montage[0], 0)
    two = build_row(montage[1], 1)

    return combine_rows(one, two, dims)


def remove_temp_files(montage):
    """remove all the temporary files"""
    to_go = ['mont0.png', 'mont1.png', f'tmp{os.getpid()}.png']
    for row in montage:
        #print("row =", row)
        files = [row[x]['name'] for x in row]
        #print("files =",files)
        to_go = to_go+files

    for x in to_go:
        os.unlink(x)
        #print(x)


def normalize_montage_images(montage, dims):
    """normalise the montage images"""
    prefix = os.getpid()
    r=0
    for row in montage:
        for i in row:
            # name = row[i]['name']
            norm = f"{prefix}_{r}_{i}.png"
            normalize_image(row[i], norm, dims)
            row[i]['name'] = norm
        r += 1


def usage():
    """usage message"""
    print("montage_wallpaper.py [-s wxh] [-l wxh] ")
    print("   -s wxh    - dimensions of wallpaper to create")
    print("   -l wxh    - layout images in montage")
    print("             - default is to generate wallpaper at 1920x1200 with layout of 5x2")
    print("             - optionally provide alternative wallpaper width and height and layout wxh")
    print("   -v        - verbose output and keep temporary files")


def validate_wxh(arg):
    """validate w,h"""
    try:
        b,c = arg.split('x')
        d=int(b)
        e=int(c)
        return (d,e), True #size = arg
    except ValueError:
        print("arg not WxH - expecting 1920x1200 for example")
    return (-1,-1), False


def getOptions(options):
    """get options"""
    # pylint: disable=too-many-branches

    try:
        long_opts = ["help", "verbose", "keep", "size=", "layout=", "display"]
        opts, args = getopt.getopt(sys.argv[1:], "hvks:l:d", long_opts)
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    options['verbose'] = False
    options['keep'] = False
    options['display'] = False

    for o, a in opts:
        if o == "-v":
            options['verbose'] = True
        elif o == "-k":
            options['keep'] = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--size"):
            size, status = validate_wxh(a)
            if status:
                options['size'] = size
        elif o in ("-l", "--layout"):
            layout, status = validate_wxh(a)
            if status:
                options['layout'] = layout
        elif o in ("-d", "--display"):
            options['display'] = True
        else:
            assert False, "unhandled option"

    #print("ARGS",args)
    if len(args) > 0:
        if os.path.isdir(args[0]):
            options['files'] = glob(args[0]+"/*.jpg")
        else:
            options['files'] = args
    else:
        options['files'] = glob('*.jpg')
    for fn in options['files']:
        if fn.find('montage_') > -1:
            options['files'].remove(fn)
    return options


def main():
    """main"""
    # pylint: disable=global-statement
    global Verbose

    options = getOptions({ 'size': (1920, 1200), 'layout': (5, 2) })
    #print("OPTIONS", options, "\n")
    Verbose = options['verbose']

    w = options['size'][0]
    h = options['size'][1]
    #layout = options['layout']
    size = f'{w}x{h}'

    dims = {'size':size,          # size
            'sw':w, 'sh':h,       # size width, size height
            'pw':w/options['layout'][0],     # portrait width
            'ph':h/options['layout'][1],     # portrait height
            'lw':w/(options['layout'][0]/2), # landscape width
            'lh':h/options['layout'][1]}     # landscape height
    #print(dims)

    if not enough_files(options['files'], options['layout']):
        print("ERROR(1): Cannot create layout with supplied images.")
        sys.exit()

    montage = create_layout(options['files'], options['layout'])
    if len(montage) != options['layout'][1]:
        print("ERROR(2): Cannot create layout with supplied images.")
        sys.exit()

    print_layout(montage)

    normalize_montage_images(montage, dims)

    verbose_print(montage)

    name = build_montage(montage, dims)

    if not options['keep']:
        remove_temp_files(montage)

    if unix('which feh')[0] == 0 and options['display']:
        unix(f'feh {name}')


if __name__ == "__main__":
    main()
