COMPOSE_DEV=docker-compose -f docker-compose.yml
COMPOSE_CYPRESS=$(COMPOSE_DEV) -f docker-compose.cypress.yml
BUILD_COMMAND=$(COMPOSE_DEV) build
UPGRADE_MIGRATIONS_COMMAND=$(COMPOSE_DEV) run --rm backend bash -c "sleep 5 && alembic upgrade head"

build:
	$(BUILD_COMMAND)
	$(UPGRADE_MIGRATIONS_COMMAND)

compile-messages:
	$(COMPOSE_DEV) run --rm  --no-deps backend pybabel compile -d locale

extract-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel extract -F babel.ini -k gettext_lazy -k _ -o locale/messages.pot .

lint: lint-backend lint-frontend

lint-backend:
	$(COMPOSE_DEV) run --rm --no-deps backend bash -c " \
		isort .; \
		black . --exclude=migrations; \
		flake8 .; \
		mypy .; \
		pylint app; \
		bandit . --exclude migrations,tests --recursive; \
	"

lint-frontend:
	$(COMPOSE_DEV) run --rm --no-deps frontend sh -c "yarn lint"

create-migration:
	$(COMPOSE_DEV) run --rm backend bash -c "sleep 5 && alembic revision --autogenerate -m '$(m)'"

upgrade-migrations:
	$(UPGRADE_MIGRATIONS_COMMAND)

setup:
	git config blame.ignoreRevsFile .git-blame-ignore-revs
	pre-commit install --hook-type pre-commit --hook-type pre-push

test: test-backend test-frontend

test-backend:
	$(UPGRADE_MIGRATIONS_COMMAND)
	$(COMPOSE_DEV) run --rm backend pytest .

test-e2e:
	$(COMPOSE_CYPRESS) up --exit-code-from e2e

test-frontend:
	$(COMPOSE_DEV) run --rm frontend sh -c "CI=true yarn test"

update-messages:
	$(COMPOSE_DEV) run --rm --no-deps backend pybabel update -i locale/messages.pot -d locale
