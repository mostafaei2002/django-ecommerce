# Full stack Django/Bootstrap Ecommerce app

## Usage With docker

1. Install docker & docker-compose
2. run `docker-compose -f docker-compose-dev.yaml up --build` in root folder
3. view website on localhost:8000

## Usage without Docker

1. Install dependencies from requirements.txt in backend folder with `pip install requirements.txt`
2. Run `python manage.py runserver` in backend folder
3. View website on localhost:8000

## Other Commands

Run the below commands inside backend folder

-   Run `python manage.py createcategories 10` to create 10 test categories
-   Run `python manage.py createproducts 100` to create 100 test products
-   Run `python manage.py createreviews 500` to create 500 test reviews
-   Run `python manage.py test` to run tests
-   Run `python manage.py createsuperuser` to create an admin user
