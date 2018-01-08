build:
	mkdir -p dist
	zip -r dist/random_numbers.zip psycopg2/
	zip -g dist/random_numbers.zip service.py
	zip -g dist/random_numbers.zip config.json

invoke:
	aws lambda invoke \
	--region us-east-1 \
	--function-name random_numbers \
	/dev/stdout

deploy: build
	aws lambda update-function-code \
	--region us-east-1 \
	--function-name random_numbers \
	--zip-file fileb://dist/random_numbers.zip

clean:
	rm -rf dist/
