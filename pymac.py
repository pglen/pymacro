#!/usr/bin/env python

import os, sys, string, argparse
import stack

'''
Macro expansions. I was looking at this state machine and I discovered that
I do not have to keep several states. Provided that I create a spec that
has unique markers for each function.

## Markers:

    Definition:

      Begin Mac     Define Body      End Mac
    ------------  --------------   -------------
    $$macro_name$$    macro_body      @@macro_name@@

    The macro body is collected from the name defintion to macro
    terminator.

    Reference the macro:

        %%macro_expansion%%

'''

 # Globals

STATE_INIT  = 0
STATE_MDEF  = 1
STATE_MBOD  = 2
STATE_MEND  = 3
STATE_EXPM  = 4

seeninc = []
seenmac = []
seenbod = []

currline = {}
currfile = []

# This class stores the state information for ...

class States_class():

    _frozen = False

    def __init__(self):
        self.state = 0;
        self.dname = [];    self.xname = []
        self.body  = [];    self.macx = []
        self.compr = [];    self.lineno = 0
        self.lines = [];    self.file = ""
        self.fname = ""
        self._frozen = True

    def __setattr__(self, attribute, value):
        if self._frozen and (not attribute in self.__dict__):
            print("Cannot set %s" % attribute)
            raise ValueError("Cannot set attribute '%s' on '%s'" % \
                                (attribute, States_class.__name__))
        else:
            self.__dict__[attribute] = value

States = States_class()

# Delimiters for the macro spec
delim = "$"; delim2 = '@'; delim3 = '%'

def esplit(strx):

    ''' Split str on single set of delimiters, and include
        the delimiter in the output '''

    arr = []; cumm = "" ; esc = False

    # Short circuit: no string or too short
    xlen = len(strx)
    if not xlen:
        return arr
    if xlen == 1:
        arr.append(strx)
        return arr

    prev = strx[0]                  # Pre load
    for aa in range(1, xlen):
        ccc = strx[aa];
        if not esc:
            if ccc == '\\':
                esc = True

            if  (ccc == delim  and prev == delim) or \
                (ccc == delim2 and prev == delim2) or \
                (ccc == delim3 and prev == delim3):
                if cumm:
                    arr.append(cumm[:-1])

                arr.append(ccc + ccc)
                cumm = ""
            else:
                if aa == 1:
                    cumm += prev
                cumm += ccc
        else:
            cumm += ccc
            esc = False
            pass
        prev = ccc

    # Left over field with no separator:
    if cumm != "":
        #print("leftover", cumm)
        arr.append(cumm)

    if args.deb > 8:
        print("esplit", "[{" + strx +"}]", "--", arr);
    return arr

def is_macro(macname):

    for bb in range(len(seenmac)):
        if seenmac[bb] == macname:
            return bb
    return -1

def lookup_macro(macname, indent = 0):

    #print("lookup_macro()", macname, indent)

    lll2 = ""
    found = 0
    for bb in range(len(seenmac)):

        #print("dump mac:",  seenmac[bb])
        #print("dump body:", seenbod[bb])

        if seenmac[bb] == macname:
            found = True
            #if args.verbose:
            #    print("\nexpand_lineing macro:", seenmac[bb],
            #            "bod:", seenbod[bb], "pos:", indent)
            cnt = 0
            for aa in seenbod[bb]:
                if not cnt:         # First line in place
                    sss =  aa
                else:
                    sss = "\n" + " " * indent + aa
                lll2 += sss
                cnt += 1

    if not found:
        print("Warning: Unknown macro: '%s'" % macname,
                    "in file:",  States.fname, "Line:", currline[States.fname],
                file=sys.stderr)
    return lll2

def  expand_line(lll, fff):

    if args.deb > 7:
        print("expand_line", "{" + lll + "'}")

    #print("line:", lll)

    States.lineno += 1
    # Short curcuit: Blank line:
    if not len(lll):
        return ""

    cnt = 0
    lll2 = ""; expos = 0;  pos = 0
    larr = esplit(lll)
    #print("larr", larr)
    for aa in larr:
        #print(" part", "'" + aa + "'", "pos", pos)
        #print("state:", States.state)

        if States.state == STATE_INIT:
            if aa == "$$":
                States.state = STATE_MDEF
                States.macx = []
            elif aa == "%%":
                States.state = STATE_EXPM
                States.xname = []
                expos = pos
            else:
                # If nothing goes on, add it to the output
                lll2 += aa

        elif States.state == STATE_MDEF:
            if aa == "$$":
                if args.deb > 5:
                    print("Define", States.macx)
                States.state = STATE_MBOD
                States.body = []
            else:
                States.macx.append(aa)

        elif States.state == STATE_EXPM:
            if aa == "%%":
                #print("Expand:", States.xname[0])
                States.state = STATE_INIT
                macbod = lookup_macro(States.xname[0], expos)
                if args.deb > 5:
                    print("Expand:", States.xname)
                    print("Macbody:",  macbod)

                if args.verbose > 1:
                    lll2 += "'''%s'''" % States.xname

                lll2 += macbod
            else:
                #print("cumm3", States.state.len(), aa)
                States.xname.append(aa)

        elif States.state == STATE_MBOD:
            if aa == "@@": # or aa == "$$":
                States.state = STATE_MEND
            else:
                # Accumulate body
                States.body.append(aa)
                States.lines.append(States.lineno)

        elif States.state == STATE_MEND:
            if aa == "@@": # or aa == "$$":

                head = "".join(States.macx)
                #print("Head:", head)
                if args.deb > 8:
                    print("Body:", States.body)
                    print("Lines:", States.lines)

                # Unify lines:
                uni = {}; body = []
                for aaa in range(len(States.body)):
                    linex = States.lines[aaa]
                    try:
                        uni[linex] += States.body[aaa]
                    except:
                        uni[linex] = ""
                        uni[linex] += States.body[aaa]
                #print("uni", uni)
                for bb in uni.keys():
                    body.append(uni[bb])

                #print("Body:", body)
                if args.deb > 5:
                    print("End def:", States.body)

                # matches current?
                #print("Closure mac:", States.macx[0])
                #print("Closure bod:", States.dname[0])

                # only if there is closure name
                if len(States.dname) and States.dname[0].strip():
                    if States.macx[0] != States.dname[0]:
                        print("Warning: Invalid closure for macro: '%s'" %  States.macx[0],
                           "in file:",  fff,  "Line:", currline[fff],
                                     file=sys.stderr)
                #if args.deb > 5:
                #    print("macx:", head)
                #    print("body:",  body)

                if States.macx[0] == "include":
                    #print("SPECIAL: include", "'" + States.body[0].strip() + "'")
                    parseincfile(States.body[0].strip(), outfp)
                    # Restore current file
                    States.fname = fff
                else:
                    # Save macro
                    if args.deb > 5:
                        print("Save mac:", head)
                        print("Save bod:", body)
                    rrr = is_macro(head)
                    if rrr >= 0 :
                        print("Warning: duplicate macro: '%s'" % head,
                            "in file:",  States.fname, "Line:", currline[States.fname],
                        file=sys.stdout)
                        seenmac[rrr] = head
                        seenbod[rrr] = body
                    else:
                        seenmac.append(head)
                        seenbod.append(body)

                # Was this an abrupt termination?
                if aa == "$$":
                    # start new macro
                    #print("New macro in body define", States.macx)
                    #States.state = STATE_MDEF
                    #States.macx = []
                    pass
                else:
                    # Reset state
                    States.body = []
                    States.lines = []
                    States.dname = []
                    States.state = 0
            else:
                States.dname.append(aa)
        else:
            if 1: #args.deb > 0:
                print("Invalid state", States.state)
            pass

        pos += len(aa)
        #print("pos:", pos, "aa:", aa)
        cnt += 1

    if lll2 == "":
        return None

    return lll2

def parseincfile(macfile, outfp):

    # Reset parser
    States.macx[0] = "" # Kill macro name, prevent recursion
    States.state = 0
    States.macx = []
    States.body = []
    States.dname = []
    States.lines = []

    # Scan possible locations

    # 1.) dir of the source file
    ppp = os.path.dirname(args.infile)
    fff = os.path.join(ppp, macfile)
    #print("try: fff", fff)
    if os.path.isfile(fff):
        seeninc.append(fff)
        if args.verbose:
            print("Including:  '%s'" % fff)
        parsefile(fff, outfp, True)

        return True

    # 2.) current dir
    if os.path.isfile(macfile):
        seeninc.append(macfile)
        if args.verbose:
            print("Including:  '%s'" % macfile)
        parsefile(macfile, outfp, True)
        return True

    # 3.) user macro dir
    ppp = os.path.dirname(os.path.expanduser("~/pymacros/"))
    fff = os.path.join(ppp, macfile)
    #print("try: fff", fff)
    if os.path.isfile(fff):
        seeninc.append(fff)
        if args.verbose:
            print("Including:  '%s'" % fff)
        parsefile(fff, outfp, True)
        return True

    print("Warning: Could not open include: '%s'" % macfile,
                    "in file:",  States.fname, "Line:", currline[States.fname],
                    file=sys.stdout)
    return False

def add_line(zstr, xstr):

    if zstr != None:
        padd = ""
        if xstr:
            padd = "\n"
        xstr += padd + zstr
    return xstr

def parsefile(nnn, outfp, inc=False):

    global currline, currfile;

    currfile.append(nnn)
    States.fname = nnn
    #print ("Parsing", nnn)

    fpi = open(nnn, "r")
    xstr = "";  addnext = "";
    for aaa in fpi:
        try:
            currline[nnn] += 1
        except:
            currline[nnn] = 1

        bbb = str.replace(aaa, "\n", "")

        if currline[nnn] <= args.skip and inc==False:
            if args.deb > 3:
                print("Skipping:", nnn, currline[nnn], bbb)
            continue

        # Macro Comment
        if str.strip(bbb)[:2] == "$#":
            #print("Comment", bbb)
            continue

        if str.strip(bbb)[:2] == "#$":
            #print("Comment", bbb)
            continue

        if str.strip(bbb)[:2] == "//$":
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

            zstr = expand_line(bbb, nnn)
            #print("zstr:", zstr)
            if args.showinput:
                print("Output: [", zstr, "]")
            xstr = add_line(zstr, xstr)

    # Left over without line continuation
    if addnext != "":
        #print("Continuation", addnext)
        zstr = expand_line (addnext, nnn)
        xstr = add_line(zstr, xstr)

    # Loop until all items are expand_lineed

    cnt = 0  # Thinking 6 deep is enough

    if xstr != None:
        cnt = 0
        while(1):
            if args.norecurse:
                break
            cnt += 1
            xstr2 = xstr.split("\n")
            xstr3 = ""
            for aa in xstr2:
                zstr = expand_line(aa, nnn)
                #print("zstr", "'" + zstr + "'")
                xstr3 = add_line(zstr, xstr3)
            if xstr3 == None:
                break
            xstr = xstr3
            if xstr2 == xstr:
                #print("No change")
                break
            if cnt > 6:
                break

        # No text on macro files

        if inc:
            return

        #print ("xstr", xstr);
        if xstr:
            print("%s" % xstr, file=outfp)

desc = '''\
Will expand macros. A macro is defined with a '$$' enclosed sting. (Like: $$macro$$)
The macro body is defined after that, terminated by a '@@' enclosed string. (like: @@macro@@)
The macro is expanded by a '%%' enclosed string. (like: %%macro%%). Here is a
complete macro with expansion. $$mac$$ Hello @@mac@@ %%mac%%.
Include search path: the path of the source file, current directory then
the global macro path. (~/pymacros).
The strings '$#' '#$' '//#' at the beginning of the line act as comments.
'''
argparser = argparse.ArgumentParser(description=desc)

argparser.add_argument( '-v',  '--verbose',
    action="count", default=0,
    help='Show operational details. -vv more for output')

argparser.add_argument( '-d',  '--deb',
    action="store", type=int, default=0,
    help='Debug level (0=none 10=Noisy)')

argparser.add_argument( '-s',  '--skip',
    action="store", type=int, default=0,
    help='Skip number of initial lines')

argparser.add_argument( '-i',  '--showinput',
    action="store_true",
    help='Show input lines from file ')

argparser.add_argument( '-n',  '--norecurse',
    action="store_true",
    help='Do not recurse. Flat expansion.')

argparser.add_argument( 'infile')
argparser.add_argument( 'outfile', nargs='?')

#print("Python Macros running on ", sys.version);

# Start of program:

if __name__ == '__main__':

    global args

    args = argparser.parse_args()
    if args.deb > 9:
        print (args)

    if args.outfile:
        if args.infile == args.outfile:
            print("Cannot use the same file as in / out")
            sys.exit(1)

    if args.outfile:
        outfp = open(args.outfile, "w")
    else:
        outfp = sys.stdout

    if args.verbose:
        print("Processing: '%s'" % args.infile)

    if not os.path.isfile(args.infile):
        print("Cannot open: '%s'"  % args.infile)
        sys.exit(0)

    parsefile(args.infile, outfp)

    # Diagnostics: print macros
    if args.deb > 4:
        print("Dumping macros:")
        for aa in range(len(seenmac)):
            print("Macro:", seenmac[aa], " = " , seenbod[aa])

    #print()

# EOF
