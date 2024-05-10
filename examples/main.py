#!/usr/bin/env python
import os, sys, string, argparse
'''
 Header. This is now an example macro source include.
'''
# Globals
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
        print("use:  prog=Program Name infile")
        sys.exit(0)
    if args.outfile:
        if args.infile == args.outfile:
            print("Cannot use the same file as in / out")
            sys.exit(1)
    # Adding Code:
    aa = 0
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

