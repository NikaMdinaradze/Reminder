install_requirements:
	@echo "Installing requirements"
	docker-compose down && docker-compose build


makemigrations:
	@echo "Making Migration files"
	python manage.py makemigrations

migrate:
	@echo "Running Migrations Docker"
	docker-compose run --rm web python manage.py migrate

build:
	@echo "building API test server docker"
	docker-compose build

run:
	@echo "starting API test server docker"
	docker-compose up

run_tests:
	@echo "running tests docker"
	docker-compose run --rm web python manage.py test

createsuperuser:
	@echo "creating super user"
	docker-compose run --rm web python manage.py createsuperuser
