mig:
	python3 manage.py makemigrations && python3 manage.py migrate

load_file:
	python3 manage.py loaddata regions.json

load_file1:
	python3 manage.py loaddata districts.json

to_json:
	python3 manage.py dumpdata apps.Region --indent 2 > region_fixture.json && python3 manage.pyKa dumpdata apps.District --indent 2 > district_fixture.json