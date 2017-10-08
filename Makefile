ifeq (, $(ENV))
	env := development
else ifeq (test, $(ENV))
	env := testing
else
	env := $(ENV)
endif

app := bregenz

# -- installation

setup:
	pip install -e '.[${env}]' -c constraints.txt
.PHONY: setup

update:
	pip install --upgrade -e '.[${env}]' -c constraints.txt
.PHONY: setup

# -- application

serve:
	./bin/serve --env development --config config/development.ini --reload
.PHONY: serve

# -- testing

test:
	ENV=test py.test -c 'config/testing.ini' -s -q
.PHONY: test

coverage:
	ENV=test py.test -c 'config/testing.ini' -s -q --cov=${app} --cov-report \
	  term-missing:skip-covered
.PHONY: coverage

# -- utility

check-flake8:
	flake8
.PHONY: check-flake8

check-pylint:
	pylint
.PHONY: check-pylint

# TODO: add `check-pylint`
check: | check-flake8
.PHONY: check

clean:
	find . ! -readable -prune -o -print \
	 ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./venv*" \
	 ! -path "./doc/*" ! -path "./locale/*" ! -path "./tmp/*" \
	 ! -path "./lib/*" | \
	 grep -E "(__pycache__|\.egg-info|\.pyc|\.pyo)" | xargs rm -rf
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	gulp clean
endif
.PHONY: clean


.DEFAULT_GOAL = coverage
default: coverage
