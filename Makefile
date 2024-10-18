.PHONY: install dev format

install:
	pip3 install -r requirements.txt

dev:
	python3 app.py

format:
	python3 -m black .; \
	python3 -m isort .;
