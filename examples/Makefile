# Make for pymac build

# We add the macro file to the inference rule, (pattern rule) to ...
# ... re-make if the macro has changed

%.py : %.mac main.inc
	../pyvmac.py  $< $@

build: main.py main.inc
	python main.py ${OPT}

# EOF
