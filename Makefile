all: requirements scrape process

development-requirements:
	pip install -r development-requirements.txt

requirements:
	pip install -r requirements.txt

scrape: clean
	scrapy crawl scale_schedule -o events.json

clean:
	rm -vf events.json events.csv README.md

process:
	python process.py | tee README.md

.PHONY: all requirements scrape clean process
