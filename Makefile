# using executable files from the virtualenv
python		:= ./.venv/bin/python
pip		:= ./.venv/bin/pip
nose		:= ./.venv/bin/nosetests
flake8		:= ./.venv/bin/flake8
cli		:= ./.venv/bin/tw-conf-parse

# main targets

default: tests
tests: smoke lint unit integration
setup: clean venv pip

# environment setup targets
clean:
	# removing git-ignored files
	@git clean -Xdfq

venv:
	# ensuring a virtualenv virtual env
	@test -x ".venv/bin/pip" || virtualenv --quiet .venv

pip:
	# installing latest pip
	@$(pip) install --quiet --upgrade pip
	# installing dev dependencies
	@$(pip) install --quiet --requirement=development.txt
	# install python module locally
	@$(python) setup.py develop

smoke:
	# checking imports for syntax errors
	@$(python) -c 'from tw_conference_manager import engine'

lint:
	# checking for code smells in main python module
	@$(flake8) tw_conference_manager

unit:
	# running unit tests and reporting coverage:
	@$(nose) --rednose --cover-erase tests/unit

integration:
	@$(cli) tests/fixtures.txt

docker:
	docker build . -t tw-code-assignment
	docker run tw-code-assignment

.PHONY: tests
