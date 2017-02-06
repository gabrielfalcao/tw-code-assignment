# using executable files from the virtualenv
python		:= ./.venv/bin/python
pip		:= ./.venv/bin/pip
nose		:= ./.venv/bin/nosetests
flake8		:= ./.venv/bin/flake8

# main targets

default: setup tests
tests: smoke unit
setup: venv pip

# environment setup targets
venv:
	# ensuring a virtualenv virtual env
	@test -x ".venv/bin/pip" || virtualenv .venv

pip:
	# installing latest pip
	@$(pip) install -qU pip
	# installing dev dependencies
	@$(pip) install -qr development.txt

smoke:
	# checking imports for syntax errors
	@$(python) -c 'from tw_conference_manager import engines'

lint:
	# checking imports for code smells
	@$(flake8) -c 'from tw_conference_manager import engines'

unit:
	# running unit tests and reporting coverage:
	@$(nose) --rednose --cover-erase tests/unit

docker:
	docker build . -t tw-code-assignment
	docker run tw-code-assignment

.PHONY: tests
