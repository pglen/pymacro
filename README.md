# pymacro

## This is a simple macro processor.

    usage: pymac.py [-h] [-v] [-d DEBUG] [-i] infile [outfile]

 Will expand macros into outfile or stdout

A macro is defined with a '\$\$' enclosed sting. [Like: \$\$macro\$\$]
The macro body is defined after that, terminated by a '@@' enclosed
string. [like: @@macro@@] The empty terminator '@@ @@' can be used as a convenience;


All the command prefixes / suffixed can be escaped with a backslash to
loose their special meaning.

The macro is expanded by a '%%' enclosed string. (like: %%macro%%).

Here is a complete example macro with expansion:

    \$\$mac\$\$ Hello @@mac@@
    %%mac%%.

## Include search path:

 * Path of the source file,
 * Current directory
 * User's macro path. (~/pymacros).

## Macro Comments:

The strings '$#' '#$' '//#' at the beginning of the line act  as comments.
Those lines are ignored and not prpagated to the output.

The defined macros then referenced by name and a leading / trailing '$%%' sign.

### Examples:

     \$\$hello\$\$ This is a macro. @@hello@@

     The above macro will be substituted here:
     %%hello%%

All other text is propagated verbatim.

 The special macro / command \$\$include\$\$ will read a macro file into the current
context.

Warnings are issued :

 * if a macro is not defined,
 * the macro had duplicate definition,
 * the macro is not terminated with the same name (except the empty terminator)
 * include file cannot be found.

  Recursive expansion. Up to six level of recursion is expanded. Make sure that there
are no self referencing macros like:

       \$\$recurse\$\$ This macro will \$\$recurse\$\$ into itself

  The recursive macro will print many copies (6) into the output. It is not planned to
catch recursion any time soon.

This is a quick hack, please do not expect much here. However this utility is a
life saver for coding.

## Example usage:

  The utility will allow you to refer to code tie a simple macro. For instance the
following code in an include file pulled in to the current context:

    \$\$include\$\$ main.inc @@include@@
    \$\$progname$$ prog="Program Name"
    @@progname@@
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

# EOF
