ifeq (, $(ENV))
	ENV := development
	env := development
else ifeq (test, $(ENV))
	env := testing
else
	env := $(ENV)
endif

ifeq (, $(NODE_ENV))
	NODE_ENV := development
endif

app := willisau

# -- installation

setup:
	pip install -e '.[${env}]' -c constraints.txt
.PHONY: setup

setup-force:
	pip install --upgrade --force-reinstall -e '.[${env}]' -c constraints.txt
.PHONY: setup-force

update:
	pip install --upgrade -e '.[${env}]' -c constraints.txt
.PHONY: update

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

check:
	flake8
.PHONY: check

lint:
	pylint test ${app}
.PHONY: lint

vet: | check lint
.PHONY: vet

analyze:
	docker run --interactive --tty --rm --env CODECLIMATE_CODE="${PWD}" \
	  --volume "${PWD}":/code \
	  --volume /var/run/docker.sock:/var/run/docker.sock \
	  --volume /tmp/cc:/tmp/cc \
	  codeclimate/codeclimate analyze -f text > tmp/codequality.txt
	cat tmp/codequality.txt
.PHONY: analyze

build:
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	NODE_ENV=$(NODE_ENV) gulp
endif
.PHONY: build

clean:
	find . ! -readable -prune -o -print \
	  ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./venv*" \
	  ! -path "./doc/*" ! -path "./locale/*" ! -path "./tmp/*" \
	  ! -path "./lib/*" | \
	  grep -E "(__pycache__|\.egg-info|\.pyc|\.pyo)" | \
	  xargs rm -rf
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	gulp clean
endif
.PHONY: clean


.DEFAULT_GOAL = coverage
default: coverage
