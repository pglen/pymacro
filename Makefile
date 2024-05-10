# pyvmac.py

clean:
	@echo "Clean"
	rm -r __pycache__
	rm -f aa bb cc

test:
	./pyvmac.py tests/mac_1.txt  > aa
	./pyvmac.py tests/mac_3.txt  >>aa
	./pyvmac.py tests/mac_5.txt  >>aa
	./pyvmac.py tests/mac_7.txt  >>aa
	./pyvmac.py tests/mac_2.txt  >>aa
	./pyvmac.py tests/mac_4.txt  >>aa
	./pyvmac.py tests/mac_6.txt  >>aa
	./pyvmac.py tests/mac_8.txt  >>aa
	diff aa test.org
	rm -f aa

preptest:
	./pyvmac.py tests/mac_1.txt  > test.org
	./pyvmac.py tests/mac_3.txt  >>test.org
	./pyvmac.py tests/mac_5.txt  >>test.org
	./pyvmac.py tests/mac_7.txt  >>test.org
	./pyvmac.py tests/mac_2.txt  >>test.org
	./pyvmac.py tests/mac_4.txt  >>test.org
	./pyvmac.py tests/mac_6.txt  >>test.org
	./pyvmac.py tests/mac_8.txt  >>test.org

AUTOCHECK="autocheck"

git: clean
	git add .
	git commit -m "$(AUTOCHECK)"
	git push
#	git push local

git2:
	@$(eval AAA=$(shell zenity --entry --text "Enter Git Commit Message:"))
	git add .
	git commit -m "${AAA}"
	git push

# EOF
