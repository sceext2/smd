# makefile, smd/

SMD_BIN=./smd

DOC_SRC=./doc/smd_格式定义_v0.1.0.smd.txt
DOC_OUT=./smd_doc.out.txt

target: clean
.PHONY: target

clean: clean_py
.PHONY: clean

clean_py:
	find . | grep "__pycache__" | xargs rm -r
.PHONY: clean_py

test: $(DOC_OUT)
.PHONY: test

$(DOC_OUT): $(DOC_SRC)
	$(SMD_BIN) $(DOC_SRC) -o $(DOC_OUT)


# end makefile


