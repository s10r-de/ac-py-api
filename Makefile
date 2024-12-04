
CONFIG=$(PWD)/config-docker.ini
DATA=$(PWD)/../data-docker

DEBUG=--debug

IMAGE_NAME=active-collab-backup
IMAGE_NAME_DEV=active-collab-backup-dev
CONTAINER_NAME=active-collab-backup
CONTAINER_NAME_DEV=active-collab-backup-dev

# docker based
docker: clean Dockerfile
	docker buildx build -f Dockerfile -t $(IMAGE_NAME) .

docker-dev: clean Dockerfile Dockerfile-dev
	docker buildx build -f Dockerfile-dev -t $(IMAGE_NAME_DEV) .

DOCKER_RUN_OPTS=run --rm -v $(CONFIG):/config.ini -v $(DATA):/data --name $(CONTAINER_NAME) $(IMAGE_NAME)
DOCKER_RUN_OPTS_DEV=run --rm -v $(CONFIG):/config.ini -v $(DATA):/data --name $(CONTAINER_NAME_DEV) $(IMAGE_NAME_DEV)

run_info: docker
	@echo "info for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) info

run_dump: docker
	@echo "dump for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) dump

run_delete: docker
	@echo "delete for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) delete

run_empty: docker
	@echo "empty for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) empty

run_load: docker
	@echo "load for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) load

run_verify: docker
	@echo "verify for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) verify

docker_test: docker-dev
	docker $(DOCKER_RUN_OPTS_DEV) /app/.venv/bin/python3 -m unittest -v

docker_lint: docker-dev
	docker $(DOCKER_RUN_OPTS_DEV) /app/.venv/bin/pylint AcDump/ active_collab_storage/ ActiveCollab/

# local venv
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
	. .venv/bin/activate; python3 -m unittest -v

lint: .venv-dev
	. .venv/bin/activate; pylint AcDump/ active_collab_storage/ ActiveCollab/

clean:
	-rm -fr .venv .pytest_cache .ruff_cache
	-find . -name "*.pyc" -delete
	-find . -name "__py*__" -delete

