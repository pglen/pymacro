#!/usr/bin/env python

import os, sys, string, argparse

'''
 Macro expansions.

'''

 # Globals

seeninc = []
seenmac = []
seenbod = []

multi = ""
multibod = ""
subnum = 0

def emptysplit(strx, delim = " "):

    ''' Split str on single delimiter '''

    arr = []; cumm = ""
    for aa in range(len(strx)):
        cumm += strx[aa];
        if strx[aa] == delim:
            arr.append(cumm)
            cumm = ""

    # Left over with no separator:
    if cumm != "":
        arr.append(cumm)

    if args.debug > 6:
        print("emptysplit", "'" + strx +"'", "--", arr);
    return arr

currline = {}
currfile = []

#print("Python Macros running on ", sys.version);

def  expand(lll, fff):

    global multi, multibod, subnum

    mac = "";  inmac = "";  lll2 = ""

    if args.debug > 5:
        print("expanding", "{" + lll + "'}")

    # In multi macro save text or eval end
    if multi != "":
        if multi in lll:
            offs = lll.find(multi)
            # Add last partial
            multibod += lll[:offs]
            # Erase last NL
            multibod = multibod[:-1]
            if args.verbose:
                print ("\nmultibod:", "[" + multibod + "]")

            seenmac.append(multi)
            seenbod.append(multibod)
            multi = ""; multibod = ""
        else:
            multibod += lll + "\n"
        return None

    for aa in emptysplit(lll):
        #print(" part", "'" + aa + "'")
        cc = str.strip(aa)
        if inmac == "" and multi == "":
            if len(cc) > 2 and cc[0] == "$" and cc[-1:] == "$":
                found = 0
                for bb in range(len(seenmac)):
                    if seenmac[bb] == cc[:-1]:
                        if args.verbose:
                            print("\nExpanding macro:", seenmac[bb], "bod:", seenbod[bb])
                        lll2 += seenbod[bb] + " "
                        subnum += 1
                        found = True
                if not found:
                    print("Warning: Unknown Macro in", "file:",  fff,
                                "Line:", currline[fff], aa, file=sys.stderr)
                    lll2 += aa
            elif len(cc) > 2 and cc[:2] == "$!":
                if args.verbose:
                    print("Multiline Macro definition", aa)
                multi = cc
            elif len(cc) > 2 and cc[0] == "$":
                if args.verbose:
                    print("Macro definition", cc, end = " ")
                inmac = cc
            else:
                if args.debug > 2:
                    print("leftover:", aa)
                lll2 += aa
        else:
            if args.verbose:
                print("mac:", "'" + aa + "'", end = " " )
            mac += aa

    # This line had a macro:
    if inmac != "":
        #print ("Macro:", inmac, "Body:", mac)
        # Special macros
        if inmac == "$include":
            macfile = str.strip(mac)
            if args.verbose:
                print("Include macro", macfile)
            if macfile in seeninc:
                print("Warning: in", fff,  "line:", currline[fff],
                    "Recursion to same file ignored:", "'" + macfile + "'", file=sys.stderr)
            else:
                ret =  parseincfile(macfile, outfp)
                if not ret:
                    print("Warning: in", fff, "line:", currline[fff],
                    "No macro file:", "'" + macfile + "'", file=sys.stderr)
        else:
            if inmac in seenmac:
                print ("Warning: in", fff, "line:", currline[fff], "macro ignored, defined already",
                                                        "'" + inmac + "'", file=sys.stderr)
            else:
                seenmac.append(inmac)
                seenbod.append(mac)
        lll2 = None

    # This line had a multi line macro:
    if multi != "":
        # Single line multi
        offs = lll.find(multi) + len(multi) + 1
        part = lll[offs:]
        #print("Singline part:", part)
        if multi in part:
            offs2 = part.find(multi) + offs - 1
            # Add last partial
            #print("Singline multi:'%s'" %lll[offs:offs2])
            multibod += lll[offs:offs2]
            if args.verbose:
                print ("\nmultibod:", "[" + multibod + "]")
            seenmac.append(multi)
            seenbod.append(multibod)
            multi = ""; multibod = ""
        else:
            # Add fist partial
            if not multibod:
                offs = lll.find(multi) + len(multi) + 1
                multibod += lll[offs:]
                return None
        return None

    if args.debug > 4:
        print ("parsed:", "'" + lll2 + "'")
    return lll2

def parseincfile(macfile, outfp):

    # Scan possible locations

    # 1.) dir of the source file
    ppp = os.path.dirname(args.infile)
    fff = os.path.join(ppp, macfile)
    #print("fff", fff)
    if os.path.isfile(fff):
        seeninc.append(fff)
        parsefile(fff, outfp)
        return True

    # 2.) current dir
    if os.path.isfile(macfile):
        seeninc.append(macfile)
        parsefile(macfile, outfp)
        return True

    # No file
    return False

def parsefile(nnn, outfp):

    global subnum, currline, currfile;

    currfile.append(nnn)
    #print ("Parsing", nnn)

    xstr = ""
    fpi = open(nnn, "r")
    addnext = "";
    for aaa in fpi:
        try:
            currline[nnn] += 1
        except:
            currline[nnn] = 1

        bbb = str.replace(aaa, "\n", "")

        # Comment
        if str.strip(bbb)[:2] == "$$":
            #print("Comment", bbb)
            continue

        if str.endswith(bbb, "\\"):
            addnext += bbb[:-1]
        else:
            if addnext != "":
                bbb = addnext + bbb
                #print("line ext:", bbb)
                addnext = ""

            if args.showinput:
                print("Input: [", bbb, "]")

            zstr = expand(bbb, nnn)
            #print("zstr:", zstr)
            if args.showinput:
                print("Output: [", zstr, "]")
            if zstr != None:
                if xstr:
                    xstr += "\n"
                xstr += zstr

    # Left over without line continuation
    if addnext != "":
        #print("Continuation", addnext)
        zstr = expand (addnext, nnn)
        if zstr != None:
            if xstr:
                xstr += "\n"
            xstr += zstr

    # Loop until all items are expanded

    cnt = 0  # Thinking 6 deep is enough

    if xstr != None:
        while(1):
            #break
            cnt += 1
            xstr2 = xstr[:]
            #print(nnn, "subnum", cnt, xstr)
            xstr3 =  expand (xstr2, nnn)
            if xstr3 == None:
                break
            xstr = xstr3
            if xstr2 == xstr:
                #print("No change")
                break
            if cnt > 6:
                break

        #print ("xstr", xstr);
        if xstr:
            print("%s" % xstr, file=outfp)

argparser = argparse.ArgumentParser(description='Macro processor')

argparser.add_argument( '-v',  '--verbose',
    action="store_true",
    help='show operational details')

argparser.add_argument( '-d',  '--debug',
    action="store", type=int, default=0,
    help='debug level')

argparser.add_argument( '-i',  '--showinput',
    action="store_true",
    help='show input fileo')

argparser.add_argument( 'infile')
argparser.add_argument( 'outfile', nargs='?')

# Start of program:

if __name__ == '__main__':

    global args
    args = argparser.parse_args()
    if args.debug > 5:
        print (args)

    if len(sys.argv) < 2:
        print("use: pymac.py infile")
        sys.exit(0)

    if args.outfile:
        if args.infile == args.outfile:
            print("Cannot use the same file as in / out")
            sys.exit(1)

    if args.outfile:
        outfp = open(sys.argv[2], "w")
    else:
        outfp = sys.stdout

    parsefile(args.infile, outfp)

    # Diagnostics: print macros
    if args.debug > 4:
        print("Dumping macros:")
        for aa in range(len(seenmac)):
            print("Macro:", seenmac[aa], " = " , seenbod[aa])

    #print()

# EOF
