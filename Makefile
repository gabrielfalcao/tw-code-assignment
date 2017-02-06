# using executable files from the virtualenv
python		:= ./.venv/bin/python
pip		:= ./.venv/bin/pip
nose		:= ./.venv/bin/nosetests
flake8		:= ./.venv/bin/flake8

# main targets

default: setup tests
tests: tests.smoke tests.unit
setup: setup.venv setup.pip

# environment setup targets
setup.venv:
	# ensuring a virtualenv virtual env
	@test -x ".venv/bin/pip" || virtualenv .venv

setup.pip:
	# installing latest pip
	@$(pip) install -qU pip
	# installing dev dependencies
	@$(pip) install -qr development.txt

tests.smoke:
	# checking imports for syntax errors
	@$(python) -c 'from tw_conference_manager import engines'

tests.lint:
	# checking imports for code smells
	@$(flake8) -c 'from tw_conference_manager import engines'

tests.unit:
	# running unit tests and reporting coverage:
	@$(nose) --rednose --cover-erase tests/unit

docker:
	docker-compose build
.PHONY: tests
