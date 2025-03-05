PYTHON_FILES := $(shell find . -type f -name \*.py)
all: requirements lint scrape process_events static_site

development-requirements: requirements
	pip install -r development-requirements.txt

requirements:
	pip install -r requirements.txt

lint:
	flake8 *.py
	pylint *.py
ifeq ($(CI),true)
	isort --check-only $(PYTHON_FILES)
	black --check $(PYTHON_FILES)
else
	isort --diff $(PYTHON_FILES)
	black --diff $(PYTHON_FILES)
endif
	docker run --rm -v $(PWD):/repo --workdir /repo rhysd/actionlint:latest -color

black:
	black $(PYTHON_FILES)

isort:
	isort $(PYTHON_FILES)

scrape: clean
	scrapy crawl scale_schedule -o events.json

clean:
	rm -vf events.json public/sorted_events.json public/events.csv public/EVENTS.md

process_events:
	echo "# Processing events"
	python process_events.py > public/EVENTS.md

static_site:
	echo "# Creating static site"
	python static_site.py

.PHONY: all requirements lint black isort scrape clean process_events static_site
