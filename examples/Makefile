all: data images

.PHONY: data images
data: great_apes.py
	python3 great_apes.py 500 1000

images:
	cp plots/* ../images/

clean:
	rm -r plots
