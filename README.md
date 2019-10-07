# pymacro

 This is a simple macro processor.

 Syntax: pymac.py infile [outfile]

 Will expand macros into outfile. The macros are defined by the '$' prefix.

 The macros are referenced by name and a leading / trailing '$' sign.

 $$ at the beginning of the line is comment. $! begins / ends a multi line macro.

 Examples:

 $hello This is a macro.

 The above line will be substituted here: $hello$

 All characters are propaged verbatim.

 Peter Glen


