# Bregenz

`/bʁeːgɛnt͡s/`


[![build status](https://gitlab.com/lupine-software/bregenz/badges/master/build.svg)](
https://gitlab.com/lupine-software/bregenz/commits/master) [![coverage report](
https://gitlab.com/lupine-software/bregenz/badges/master/coverage.svg)](
https://gitlab.com/lupine-software/bregenz/commits/master)

```txt
 , __
/|/  \
 | __/ ,_    _   __,  _   _  _    __
 |   \/  |  |/  /  | |/  / |/ |  / / _
 |(__/   |_/|__/\_/|/|__/  |  |_/ /_/
                  /|               /|
                  \|               \|

Bregenz; BaRe concEpt paGE applicatioN bregenZ
```

The website of [https://try.scrolliris.com/](https://try.scrolliris.com/).


## Requirements

* Python `3.5.4` (or `>= 2.7.13`)
* Node.js `7.10.1` (npm `5.4.2`, for build assets)
* [Konstanz](https://gitlab.com/lupine-software/konstanz) as git subtree


## Integrations

* Typekit
* Scrolliris (badge)


## Setup

```zsh
: setup python environment (e.g. virtualenv)
% python3.5 -m venv venv
% source venv/bin/activate
(venv) % pip install --upgrade pip setuptools

: node.js (e.g. nodeenv)
(venv) % pip install nodeenv
(venv) % nodeenv --python-virtualenv --with-npm --node=7.10.1
: re-activate for node.js at this time
(venv) % source venv/bin/activate
(venv) % npm install --global npm@5.4.2
(venv) % npm --version
5.4.2
```

### Dependencies

#### Konstanz

See article project [Konstanz](
https://gitlab.com/lupine-software/konstanz).

Don't commit directly the changes on above article project into this repo.

```zsh
: setup `doc`
% git remote add konstanz https://gitlab.com/lupine-software/konstanz.git
% git subtree add --prefix doc/article konstanz master

: synchronize with updates into specified branch
% git pull -s subtree -Xsubtree=doc/article konstanz master

: subtree list
% git log | grep git-subtree-dir | tr -d ' ' | cut -d ":" -f2 | sort | uniq
```


## Development

Use `waitress` as wsgi server.  
See `Makefile`.

```zsh
% cd /path/to/bregenz
% source venv/bin/activate

: set env
(venv) % cp .env.sample .env

: install packages
(venv) % ENV=development make setup

: install node modules & run gulp task
(venv) % npm install --global gulp-cli
(venv) % npm install

(venv) % gulp

: run server
(venv) % make serve
```

### Style check & lint

* flake8
* pylint
* eslint

```zsh
: add hook
(venv) % flake8 --install-hook git

: run make check target
(venv) % make check
```


## Deployment

Use `CherryPy` as wsgi server.

```zsh
: run install and start server for production
(venv) % ENV=production make setup

: or start server by yourself
(venv) % ./bin/serve --env production --config config/production.ini --install
```

### Delivery

E.g. Google App Engine

```zsh
: this script install cloud sdk into `./lib` directory
(venv) % ./bin/setup-google-cloud-sdk
```

Above script is equivalent following steps.

```zsh
: take latest sdk from https://cloud.google.com/sdk/downloads
% cd lib
(venv) % curl -sLO https://dl.google.com/dl/cloudsdk/channels/rapid/ \
  downloads/google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz

: check sha256 checksum
(venv) % echo "CHECKSUM" "" ./google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz \
  | sha256sum -c -
./google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz: OK
(venv) % tar zxvf google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz

: setup lib/ as a root for sdk
(venv) % CLOUDSDK_ROOT_DIR=. ./google-cloud-sdk/install.sh
(venv) % cd ../
```

```zsh
: publish website (create `app.yaml`)
(venv) % source ./bin/load-gcloud
(venv) % gcloud app deploy ./app.yaml --project <project-id> --verbosity=info
```

E.g. Heroku

```zsh
(venv) % echo '3.6.X' >> ./runtime.txt
(venv) % git push heroku master
```


## Testing

```zsh
(venv) % make test
```

### CI

You can check it by yourself using `gitlab-ci-multi-runner` on locale machine.
It requires `docker`.

```zsh
% ./bin/setup-gitlab-ci-multi-runner

: use script
% ./bin/ci-runner test
```

#### Links

See documents.

* https://gitlab.com/gitlab-org/gitlab-ci-multi-runner/issues/312
* https://docs.gitlab.com/runner/install/linux-manually.html


## Documentation

TODO


## Translation

TODO


## License

Bregenz; Copyright (c) 2017 Lupine Software LLC

This is free software;  
You can redistribute it and/or modify it under the terms of the
GNU Affero General Public License (AGPL).

See [LICENSE](LICENSE).
