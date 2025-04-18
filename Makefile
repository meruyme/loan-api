run-migrations:
	docker compose exec web python manage.py makemigrations
	docker compose exec web python manage.py migrate

update-deps:
	python -m piptools compile -o requirements.txt pyproject.toml

install-deps:
	pip-sync requirements.txt

local-up:
	docker compose up -d
	sleep 5
	docker compose exec web python manage.py migrate

test:
	USE_WEAK_PASSWORD_HASHER=1 python manage.py test --verbosity=0 --failfast

testfile:
	USE_WEAK_PASSWORD_HASHER=1 python manage.py test $(NAME) --failfast

local-test:
	docker compose exec web make test

local-testfile:
	docker compose exec web make testfile
