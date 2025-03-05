all: requirements scrape process static

development-requirements: requirements
	pip install -r development-requirements.txt

requirements:
	pip install -r requirements.txt

lint:
	flake8 *.py
	pylint *.py
ifeq ($(CI),true)
	isort --check-only *.py
	black --check *.py
else
	isort --diff *.py
	black --diff *.py
	docker run --rm -v $(PWD):/repo --workdir /repo rhysd/actionlint:latest -color
endif

black:
	black *.py

isort:
	isort *.py

scrape: clean
	scrapy crawl scale_schedule -o events.json

clean:
	rm -vf events.json public/sorted_events.json public/events.csv public/EVENTS.md

process:
	echo "# Processing events"
	python process_events.py > public/EVENTS.md

static:
	echo "# Creating static site"
	python create_static_site.py

.PHONY: all requirements scrape clean process
