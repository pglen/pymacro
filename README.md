# PyvMacro

## This is a simple macro processor.

    usage: pymac.py [-h] [-v] [-d DEB] [-s SKIP] [-i] [-n] infile [outfile]

Will expand macros into outfile or stdout

A macro is defined with a '\$\$' enclosed sting.

        $$macro_name$$

The macro body definition starts after that, terminated by a '@@' enclosed string.

        @@macro_name@@

 The empty terminator '@@ @@' can be used as a convenience;

The macro is expanded by a '%%' enclosed string.

        %%macro_name%%

Here is a complete example macro with expansion:

    $$mac$$ Hello World @@mac@@
    %%mac%%

Will print the infamous message string.

## Command arguments:

    usage: pyvmac.py [-h] [-v] [-d DEB] [-s SKIP] [-i] [-n] infile [outfile]

      positional arguments:
      infile                The main macro file
      outfile               Using stdout if omitted

    options:
      -h, --help            show this help message and exit
      -v, --verbose         Show operational details. -vv for more output
      -d DEB, --deb DEB     Debug level (0=none 10=Noisy)
      -s SKIP, --skip SKIP  Skip number of initial lines
      -i, --showinput       Show input lines from file
      -n, --norecurse       Do not recurse. Flat expansion.

Verbose prints file name as it is processed, double verbose injects the macro name
into the target as it is expanded. For troubleshooting only.

Debug outputs parsing information. Lot of info ... for advanced users or troubleshooting.

Skip lines will ignore the number of leading lines, for instance the #!/usr/bin ..
may be skipped with this option.


## Macro expansion

The defined macros then referenced by name and a leading / trailing '%%' sign.

### Examples:

     $$hello$$ This is a macro. @@hello@@
     The above macro will be substituted below:
     %%hello%%

## Macro Comments:

The strings '$#' '#$' '//#' at the beginning of the line denote comments.
Those lines are completely ignored and not propagated to the output.

## Include macro files:

The special macro / command will read a macro file into the current context.

    $$include$$ includefilename @@include@@

The include files do not contribute directly to the output, they define macros
for the main file to expand. This is to allow raw files to be annotated without
generating clutter.

The Include search path:

 * Path of the source file,
 * Current directory,
 * User's macro path (~/pymacros).

## Misc:

PyvMacro is case senstive.

All the commands prefixes / suffixes can be escaped with a backslash to
loose their special meaning.

Warnings are issued to stderr, if a:

 * Macro was referenced, but not defined,
 * Macro replaced by a duplicate definition,
 * Macro is not terminated with the same name (except the empty terminator),
 * Include file is not found.

The indentation of the macro and its definiton indentation are preserved. The
indentation in the target file is determined by the indentation of the expansion,
added to the indentation of the macro definition. In short, the program will do the
right thing for python code.

Recursive expansion. Up to six level of recursion is expanded. Make sure that there
are no self referencing macros like:

      $$recurse$$ This macro will $$recurse$$ into itself

The recursive macro will print many copies (6) into the output. It is not planned to
catch self recursion any time soon.

Preseved spaces. The delimiter is the absolute limit for the macro name / body. The
whitespce within space is preserved.

    $$macro$$ is different from $$ macro $$

This program is a quick conjure, please do not expect much here. However this utility is a
life saver for coding.

## Example usage:

  The utility will allow you to refer to code with a simple macro. For instance the
following code in an include file pulled in to the current context:

    $$include$$ main.inc @@include@@
    $$progname$$ prog="Program Name" @@progname@@
    $$code$$# Adding Code:
    aa = 0
    @@code@@
    %%xprologue%%
    %%xmain%%

Will create the following code: (from main.inc):

    !/usr/bin/env python
    import os, sys, string, argparse
    '''
     Header
    '''
    # Globals
    # Start of program:
    if __name__ == '__main__':
        global args
        args = argparser.parse_args()
        if args.debug > 5:
            print (args)
        if len(sys.argv) < 2:
            print("use:  prog="Program Name" infile")
            sys.exit(0)
        if args.outfile:
            if args.infile == args.outfile:
                print("Cannot use the same file as in / out")
                sys.exit(1)
        # Adding Code:
        aa = 0

 See the examples in tests, (mac_1.txt ... mac_N.txt) for more info.

 Peter Glen

// EOF
