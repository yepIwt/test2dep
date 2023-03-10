TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = app

all:
	@echo "make lint		- Check code with pylint"
	@echo "make format		- Reformat code with isort and black"
	@echo "make migrate		- Do all migrations in database"
	@echo "make revision	- Create new revision automatically"
	@echo "make test		- Test application with pytest"
	@echo "make test-cov	- Test application with pytest and create coverage report"
	@exit 0

clean:
	rm -fr *.egg-info dist

lint:
	pylint $(CODE)

format:
	isort $(CODE)
	black $(CODE)

run:
	uvicorn app.__main__:app --reload --port=8080 --host=0.0.0.0


revision:
	alembic -c app/db/alembic.ini revision --autogenerate

open_db:
	docker exec -it terminator_db_1 psql -U postgres -d backend_db_1

upgrade_head:
	alembic -c app/db/alembic.ini upgrade head

downgrade:
	alembic -c app/db/alembic.ini downgrade -1

	
test: db
	$(TEST)

test-cov: db
	$(TEST) --cov=app
