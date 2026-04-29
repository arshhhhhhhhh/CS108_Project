REPORT = report
TEX = pdflatex

all:
	$(TEX) $(REPORT).tex
	$(TEX) $(REPORT).tex

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz

fresh: clean all

open: all
	open $(REPORT).pdf