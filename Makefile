.PHONY: build up down logs shell migrate collectstatic

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

collectstatic:
	docker-compose exec web python manage.py collectstatic --no-input

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

restart:
	docker-compose restart

ps:
	docker-compose ps 