COMPOSE_DEV=docker-compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE_CYPRESS=$(COMPOSE_DEV) -f docker-compose.cypress.yml

build:
	$(COMPOSE_DEV) build

compile-messages:
	$(COMPOSE_DEV) run --rm  --no-deps backend pybabel compile -d locale

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

create-migration:
	$(COMPOSE_DEV) run --rm backend alembic revision --autogenerate -m '$(m)'

migrate:
	$(COMPOSE_DEV) run --rm backend alembic upgrade head

remove:
	$(COMPOSE_DEV) down

run:
	$(COMPOSE_DEV) up

setup:
	git config blame.ignoreRevsFile .git-blame-ignore-revs
	pre-commit install --hook-type pre-commit --hook-type pre-push

test: test-backend test-frontend

test-backend:
	$(COMPOSE_DEV) run --rm backend pytest .

test-e2e:
	$(COMPOSE_CYPRESS) up --exit-code-from e2e

test-frontend:
	$(COMPOSE_DEV) run --rm frontend sh -c "CI=true yarn test"

update-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel update -i locale/messages.pot -d locale
