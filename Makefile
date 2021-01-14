topologies.pdf: topologies.tex topologies.bib images/*
	pdflatex --shell-escape topologies.tex
	bibtex --shell-escape topologies
	pdflatex --shell-escape topologies.tex
	pdflatex --shell-escape topologies.tex

clean:
	rm -f *.log *.aux *.bbl *.blg
