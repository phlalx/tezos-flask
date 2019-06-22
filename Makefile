
all:
	python3 service.py

browser:
	open -a safari http://localhost:5000/index.html

clean:
	rm -rf __pycache__

