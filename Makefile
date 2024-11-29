
.venv: .venv/touchfile

.venv-dev: .venv/touchfile-dev

.venv/touchfile: requirements.txt
	test -d .venv || python3 -m venv .venv
	. .venv/bin/activate; pip3 install -r requirements.txt
	touch .venv/touchfile

.venv/touchfile-dev: .venv requirements-dev.txt
	@echo "build for DEVELOPMENT..."
	. .venv/bin/activate; pip3 install -r requirements-dev.txt
	touch .venv/touchfile-dev

test: .venv-dev
	. .venv/bin/activate; pytest tests/

lint: .venv-dev
	. .venv/bin/activate; pylint AcDump/ AcStorage/ ActiveCollab/

clean:
	-rm -fr .venv
	-find . -name "*.pyc" -delete
	-find . -name "__py*__" -delete

