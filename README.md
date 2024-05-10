# pymacro

## This is a simple macro processor.

    usage: pymac.py [-h] [-v] [-d DEBUG] [-i] infile [outfile]

 Will expand macros into outfile or stdout

A macro is defined with a '$$' enclosed sting. (Like: $$macro$$)
The macro body is defined after that, terminated by a '@@' enclosed
string. (like: @@macro@@)

The macro is expanded by a '%%' enclosed string. (like: %%macro%%).

Here is a complete example macro with expansion:

    $$mac$$ Hello @@mac@@
    %%mac%%.

## Include search path:

 * the path of the source file,
 * current directory
 * the user's macro path. (~/pymacros).

## Comments:

The strings '$#' '#$' '//#' at the beginning of the line act  as comments.
Those lines are ignored.

The defined macros than referenced by name and a leading / trailing '$%%' sign.

### Examples:

     $$hello$$ This is a macro. @@hello@@

     The above macro will be substituted here:
     %%hello%%

All other text is propagated verbatim.

 The special macro / command $$include$$ will read a macro file into the current
context.

Warnings are issued :

 *if a macro is not defined,
 * the macro had duplicate definition.
 * the macro is not terminated with the same name (except the empth terminator)
 * include file cannot be found.

  Recursive expansion. Up to six level of recursion is expanded. Make sure that there
are no self referencing macros like:

       $$recurse$$ This macro will $$recurse$$ into itself

  The recursive macro will print many copies (6) into the output. It is not planned to
catch recursion any time soon.

This is a quick hack, please do not expect professional quality. However
this utility is a life saver for coding.

 See examples in tests, (mac_1.txt ... mac_N.txt) for more info.

 Peter Glen

# EOF
