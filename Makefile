ADD_TEST_USERS_COMMAND=$(COMPOSE_DEV) exec -T postgres psql --username=postgres postgres -c "$(shell cat backend/sql/insert-test-users.sql)"

DOCKER_REPO=059132655198.dkr.ecr.eu-central-1.amazonaws.com/project-starter
DOCKER_TAG=$(shell python config/deploy/scripts/generate_tag.py)
AWS_PROFILE=default
AWS_REGION=eu-central-1

COMPOSE_PATH=config/compose/
COMPOSE_FILE=$(COMPOSE_PATH)docker-compose.yml
COMPOSE_DEV_FILE=$(COMPOSE_PATH)docker-compose.dev.yml
COMPOSE_PROD_FILE=$(COMPOSE_PATH)docker-compose.prod.yml
COMPOSE_E2E_FILE=$(COMPOSE_PATH)docker-compose.e2e.yml
COMPOSE_PROD_ARGS=DOCKER_REPO=$(DOCKER_REPO) DOCKER_TAG=$(DOCKER_TAG)

COMPOSE_DEV=docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV_FILE)
COMPOSE_PROD=$(COMPOSE_PROD_ARGS) docker compose -f $(COMPOSE_PROD_FILE)
COMPOSE_E2E=$(COMPOSE_PROD_ARGS) docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_PROD_FILE) -f $(COMPOSE_E2E_FILE)

add-test-users:
	$(ADD_TEST_USERS_COMMAND)

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
	$(COMPOSE_DEV) run --rm backend alembic revision --autogenerate -m '$(m)'

extract-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel extract -F babel.ini -k gettext_lazy -k _ -o locale/messages.pot .

lint: lint-backend lint-frontend

lint-backend:
	$(COMPOSE_DEV) run --rm --no-deps backend bash -c " \
		isort . --check-only && \
		black . --check --exclude=migrations && \
		flake8 . && \
		mypy . && \
		pylint app && \
		bandit . --exclude migrations,tests --recursive \
	"

lint-frontend:
	$(COMPOSE_DEV) run --rm --no-deps frontend sh -c "yarn lint"

migrate:
	$(COMPOSE_DEV) run --rm backend alembic upgrade head

push:
	aws ecr get-login-password --region $(AWS_REGION) --profile $(AWS_PROFILE) | docker login --username AWS --password-stdin $(DOCKER_REPO)
	$(COMPOSE_PROD) push

remove:
	$(COMPOSE_DEV) down --remove-orphans

run:
	$(COMPOSE_DEV) up

setup:
	git config blame.ignoreRevsFile .git-blame-ignore-revs
	pre-commit install --hook-type pre-commit --hook-type pre-push

test: test-backend test-frontend

test-backend:
	$(COMPOSE_DEV) run --rm backend pytest .

test-e2e:
	$(COMPOSE_E2E) up -d
	sleep 5 # Wait for migration to complete, TODO: Make waiting smarter
	$(ADD_TEST_USERS_COMMAND)
	$(COMPOSE_E2E) up --exit-code-from e2e

test-frontend:
	$(COMPOSE_DEV) run --rm frontend sh -c "CI=true yarn test"

update-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel update -i locale/messages.pot -d locale
