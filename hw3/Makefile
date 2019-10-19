srcdir  = .

main = hw3_response
figs = $(wildcard figs/*)

pdf : $(main).pdf
.PHONY: pdf

%.pdf: %.tex $(figs)
	texfot pdflatex -shell-escape $(main).tex

clean :
	rm -rf *.pdf *.aux *.out *.log _minted*
