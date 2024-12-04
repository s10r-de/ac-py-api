
CONFIG=$(PWD)/config-docker.ini
DATA=$(PWD)/../data-docker

DEBUG=--debug

IMAGE_NAME=active-collab-backup
IMAGE_NAME_DEV=active-collab-backup-dev
CONTAINER_NAME=active-collab-backup
CONTAINER_NAME_DEV=active-collab-backup-dev

# docker based
docker: Dockerfile
	docker buildx build -f Dockerfile -t $(IMAGE_NAME) .

docker-dev: Dockerfile-dev
	docker buildx build -f Dockerfile-dev -t $(IMAGE_NAME_DEV) .

DOCKER_RUN_OPTS=run --rm -v $(CONFIG):/config.ini -v $(DATA):/data --name $(CONTAINER_NAME) $(IMAGE_NAME)
DOCKER_RUN_OPTS_DEV=run --rm -v $(CONFIG):/config.ini -v $(DATA):/data --name $(CONTAINER_NAME_DEV) $(IMAGE_NAME_DEV)

docker_run_info: docker
	@echo "info for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) info

docker_run_dump: docker
	@echo "dump for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) dump

docker_run_delete: docker
	@echo "delete for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) delete

docker_run_empty: docker
	@echo "empty for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) empty

docker_run_load: docker
	@echo "load for localhost"
	docker $(DOCKER_RUN_OPTS) -c /config.ini $(DEBUG) load


docker_test: docker-dev
	docker $(DOCKER_RUN_OPTS_DEV) /app/.venv/bin/python3 -m unittest -v

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
	. .venv/bin/activate; pylint AcDump/ AcStorage/ ActiveCollab/

clean:
	-rm -fr .venv
	-find . -name "*.pyc" -delete
	-find . -name "__py*__" -delete

