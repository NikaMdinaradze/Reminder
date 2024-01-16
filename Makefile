migrations:
	@echo "Making Migration files"
	docker-compose run --rm web python manage.py makemigrations

migrate:
	@echo "Running Migrations Docker"
	docker-compose run --rm web python manage.py migrate

build:
	@echo "building API test server docker"
	docker-compose build

run:
	@echo "starting API test server docker"
	docker-compose run --rm web python manage.py migrate&&docker-compose up

run_tests:
	@echo "running tests docker"
	docker-compose run --rm web python manage.py test

createsuperuser:
	@echo "creating super user"
	docker-compose run --rm web python manage.py createsuperuser
