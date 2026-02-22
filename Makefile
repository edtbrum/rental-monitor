run:
	flask --debug run

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

shell:
	flask shell