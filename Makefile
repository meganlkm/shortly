default: test

build:
	sh build.sh

deploy:
	python deploy.py

test:
	sh run-tests.sh

setup:
	pip install --upgrade pip virtualenv
	pip install -r requirements-test.txt
	pip install --editable .
