# pymacro

## This is a simple macro processor.

    usage: pymac.py [-h] [-v] [-d DEBUG] [-i] infile [outfile]

 Will expand macros into outfile. Macros are defined by the '$' prefix.

 The defined macros than referenced by name and a leading / trailing '$' sign.

 $$ at the beginning of the line is comment. $! begins / ends a multi line macro.

### Examples:

     $hello This is a macro.
     The above macro will be substituted here: $hello$
     All other text is propagated verbatim.

    $!multi hello This is a multi line macro.
    $!multi

 The above lines will be substituted here: $!multi$

 The special macro / command $include will read a macro file into the current
context.

  Warnings are issued if a macro is not defined, or the macro had duplicate definition.
Also warnings are issued if the include file cannot ne read.

  Recursive expansion. Up to six level of recursion is expanded. Make sure that there
are no self referencing macros like:

       $recurse This macro will $recurse into itself

  The recursive macro will print many copies (6) into the output. It is not planned to
catch recursion any time soon.

This is a quick hack, please do not expect professional quality. However
this utility is a life saver for coding.

 See examples (mac_*.txt) for more info.

 Peter Glen

# EOF
