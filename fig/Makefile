minted-snippet.png: minted-snippet.tex
	pdflatex -shell-escape minted-snippet.tex
	pdftoppm -singlefile -png -r 300 minted-snippet.pdf minted-snippet

showcase.pdf: showcase.py minted-snippet.png
	python3 showcase.py

clean:
	rm -f *.log *.dvi *.aux
	rm -fr _minted-*

mrproper:
	rm -f *.ps *.pdf *.png
