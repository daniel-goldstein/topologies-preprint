topologies.pdf: topologies.tex topologies.bib images/*
	pdflatex topologies.tex
	bibtex topologies
	pdflatex topologies.tex
	pdflatex topologies.tex

clean:
	rm -f *.log *.aux *.bbl *.blg
