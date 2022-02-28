COMPOSE_DEV=docker-compose -f docker-compose.yml
BUILD_COMMAND=$(COMPOSE_DEV) build
UPGRADE_MIGRATIONS_COMMAND=$(COMPOSE_DEV) run --rm backend bash -c "sleep 5 && alembic upgrade head"

build:
	$(BUILD_COMMAND)
	$(UPGRADE_MIGRATIONS_COMMAND)

compile-messages:
	$(COMPOSE_DEV) run --rm backend pybabel compile -d locale

extract-messages:
	$(COMPOSE_DEV) run --rm backend pybabel extract -F babel.ini -k gettext_lazy -k _ -o locale/messages.pot .

lint-backend:
	$(COMPOSE_DEV) up -d backend
	$(COMPOSE_DEV) exec -T backend isort .
	$(COMPOSE_DEV) exec -T backend black . --exclude=migrations
	$(COMPOSE_DEV) exec -T backend flake8 .
	$(COMPOSE_DEV) exec -T backend mypy .
	$(COMPOSE_DEV) exec -T backend pylint app
	$(COMPOSE_DEV) exec -T backend bandit --exclude tests --exclude migrations --recursive .

create-migration:
	$(COMPOSE_DEV) run --rm backend bash -c "sleep 5 && alembic revision --autogenerate -m '$(m)'"

upgrade-migrations:
	$(UPGRADE_MIGRATIONS_COMMAND)

setup:
	git config blame.ignoreRevsFile .git-blame-ignore-revs
	pre-commit install --hook-type pre-commit --hook-type pre-push

test-backend:
	$(BUILD_COMMAND)
	$(UPGRADE_MIGRATIONS_COMMAND)
	$(COMPOSE_DEV) run --rm backend pytest .

update-messages:
	$(COMPOSE_DEV) run --rm backend pybabel update -i locale/messages.pot -d locale
