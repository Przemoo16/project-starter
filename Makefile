DOCKER_REPO=059132655198.dkr.ecr.eu-central-1.amazonaws.com/project-starter
DOCKER_TAG=$(shell python config/deploy/scripts/generate_tag.py)

COMPOSE_PATH=config/compose/
COMPOSE_FILE=$(COMPOSE_PATH)docker-compose.yml
COMPOSE_DEV_FILE=$(COMPOSE_PATH)docker-compose.dev.yml
COMPOSE_PROD_FILE=$(COMPOSE_PATH)docker-compose.prod.yml
COMPOSE_E2E_FILE=$(COMPOSE_PATH)docker-compose.e2e.yml

COMPOSE_DEV=docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV_FILE)
COMPOSE_PROD=DOCKER_REPO=$(DOCKER_REPO) DOCKER_TAG=$(DOCKER_TAG) docker compose -f $(COMPOSE_PROD_FILE)
COMPOSE_E2E=docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_E2E_FILE)

build:
	$(COMPOSE_DEV) build

build-e2e:
	$(COMPOSE_E2E) build

build-prod:
	$(COMPOSE_PROD) build

compile-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel compile -d locale

confirm-email:
	$(COMPOSE_DEV) exec -T postgres psql --username=postgres postgres -c "UPDATE public.user SET confirmed_email = TRUE WHERE email = '$(EMAIL)';"

create-migration:
	$(COMPOSE_DEV) run --rm backend alembic revision --autogenerate --message '$(MESSAGE)'

deploy:
	python -m pip install --upgrade pip
	pip install -r config/deploy/scripts/requirements.txt
	python config/deploy/scripts/deployment.py

extract-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel extract -F babel.ini -k gettext_lazy -k _ -o locale/messages.pot .

lint: lint-backend lint-frontend

lint-backend:
	$(COMPOSE_DEV) run --rm --no-deps backend bash -c " \
		find . -name '*.py' -not -path '*migrations*' -type f | xargs pyupgrade --py311-plus && \
		isort . --check-only && \
		black . --check --exclude=migrations && \
		ruff . && \
		mypy . && \
		pylint app && \
		bandit . -c pyproject.toml --recursive \
	"

lint-frontend:
	$(COMPOSE_DEV) run --rm --no-deps frontend sh -c "yarn lint"

migrate:
	$(COMPOSE_DEV) run --rm backend alembic upgrade head

push:
	aws ecr get-login-password | docker login --username AWS --password-stdin $(DOCKER_REPO)
	$(COMPOSE_PROD) push

remove:
	$(COMPOSE_DEV) down --remove-orphans

run:
	$(COMPOSE_DEV) up

setup:
	git config blame.ignoreRevsFile .git-blame-ignore-revs
	pre-commit install

stop:
	$(COMPOSE_DEV) stop

test: test-backend test-frontend

test-backend:
	$(COMPOSE_DEV) run --rm backend pytest .

test-e2e:
	$(COMPOSE_E2E) up --exit-code-from e2e

test-frontend:
	$(COMPOSE_DEV) run --rm frontend bash -c "CI=true yarn test"

update-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel update -i locale/messages.pot -d locale
