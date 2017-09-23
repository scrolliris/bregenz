ifeq (, $(ENV))
	env := development
else ifeq (test, $(ENV))
	env := testing
else
	env := $(ENV)
endif

app := bregenz

# install

setup:
	pip install -e '.[${env}]' -c constraints.txt
.PHONY: setup

# server

serve:
	./bin/serve --env development --config config/development.ini --reload
.PHONY: serve

# test

test:
	ENV=test py.test -c 'config/testing.ini' -s -q
.PHONY: test

coverage:
	ENV=test py.test -c 'config/testing.ini' -s -q --cov=${app} --cov-report \
	  term-missing:skip-covered
.PHONY: coverage

# util

check:
	flake8
.PHONY: check

clean:
	find . ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./venv*" \
	 ! -path "./doc/*"  ! -path "./tmp/*" | \
	 grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	gulp clean
endif
.PHONY: clean


.DEFAULT_GOAL = coverage
default: coverage
