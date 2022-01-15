COMPOSE_DEV=docker-compose -f docker-compose.yml
UPGRADE_MIGRATIONS=$(COMPOSE_DEV) run --rm backend bash -c "sleep 5 && alembic upgrade head"

build:
	$(COMPOSE_DEV) build
	$(UPGRADE_MIGRATIONS)

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
	${UPGRADE_MIGRATIONS}

run:
	$(COMPOSE_DEV) up -d

setup:
	git config blame.ignoreRevsFile .git-blame-ignore-revs
	pre-commit install --hook-type pre-commit --hook-type pre-push

test-backend:
	$(COMPOSE_DEV) run --rm backend pytest .
