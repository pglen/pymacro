#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

#import sys
#!/usr/bin/python

import os, sys, string
from datetime import date

seeninc = []
seenmac = []
seenbod = []

multi = ""
multibod = ""
subnum = 0

def emptysplit(strx, delim = " "):
    arr = []; cumm = ""

    for aa in range(len(strx)):
        cumm += strx[aa];
        if strx[aa] == delim:
            arr.append(cumm)
            cumm = ""

    # Left over with no separator:
    if cumm != "":
        arr.append(cumm)

    #print("arr", arr);
    return arr

#print("Python Macros running on ", sys.version);

def  expand(lll, fff, outfp):

    global multi, multibod, subnum

    mac = "";  inmac = "";  lll2 = ""

    if multi != "":
        if multi in lll:
            # Erase last NL
            multibod = multibod[:-1]
            seenmac.append(multi)
            seenbod.append(multibod)
            multi = ""; multibod = ""
        else:
            multibod += lll + "\n"
            #print ("multibod", multibod)
        return ""

    #print("expanding", "'" + lll + "'")

    for aa in emptysplit(lll):
        #print(" www", aa)
        cc = str.strip(aa)
        if inmac == "" and multi == "":
            if len(cc) > 2 and cc[0] == "$" and cc[-1:] == "$":
                xxx = 0
                for bb in range(len(seenmac)):
                    if seenmac[bb] == cc[:-1]:
                        #print("Expanding macro:", seenmac[bb], "bod:", seenbod[bb])
                        lll2 += seenbod[bb] + " "
                        subnum += 1
                        xxx = 1
                if xxx == 0:
                    print("Unknown Macro:", aa, file=sys.stderr)
                    lll2 += aa
            elif len(cc) > 2 and cc[:2] == "$!":
                #print("Multiline Macro definition", aa)
                multi = cc
            elif len(cc) > 2 and cc[0] == "$":
                #print("Macro definition", aa)
                inmac = cc
            else:
                lll2 += aa
        else:
            mac += aa

    # This line had a macro:
    if inmac != "":
        #print ("Macro:", inmac, "Body:", mac)
        # Special macros
        if inmac == "$include":
            #print("Include macro")
            macfile = str.strip(mac)
            if macfile in seeninc:
                print("Warning: in", fff,
                            "Recursion to same file ignored:", "'" + macfile + "'", file=sys.stderr)
            else:
                seeninc.append(macfile)
                parse(macfile, outfp)
        else:
            if inmac in seenmac:
                print ("Warning: in", fff, "macro defined already:", "'"+inmac+"'", file=sys.stderr)
            else:
                seenmac.append(inmac)
                seenbod.append(mac)
    # This line had a multi line macro:
    elif multi != "":
        pass
    else:
        #print("lll2:", lll2)
        if lll2[:-1] != "\n":
            lll2 += "\n"

    #print ("parsed:", "'" + lll2 + "'")
    return lll2

def parse(nnn, outfp):

    global subnum ;
    xstr = ""
    #print ("Parsing", nnn)
    fpi = open(nnn, "r")

    addnext = "";
    for aaa in fpi:
        #if 1 or aaa != "\n":
        bbb = string.replace(aaa, "\n", "")

        # Comment
        if str.strip(bbb)[:2] == "$$":
            #print("Comment", bbb)
            continue

        if str.endswith(bbb, "\\"):
            addnext += bbb[:-1]
            #print("line ext")
        else:
            if addnext != "":
                bbb = addnext + bbb
                addnext = ""
            xstr += expand (bbb, nnn, outfp)

    # Left over
    if addnext != "":
        xstr += expand (addnext, nnn, outfp)

    # Loop until all items are expanded
    while(1):
        subnum = 0;
        xstr =  expand (xstr, nnn, outfp)
        if subnum == 0:
            break

    #print ("xstr", xstr);
    print("%s" % xstr, file=outfp)


# Start of program:

if __name__ == '__main__':

    outfp = sys.stdout

    if len(sys.argv) > 2:
        outfp = open(sys.argv[2], "w")

    parse(sys.argv[1], outfp)

    # Diagnostics: print macros
    for aa in range(len(seenmac)):
        print(seenmac[aa], " = " , seenbod[aa])

    #print()


