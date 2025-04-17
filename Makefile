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
