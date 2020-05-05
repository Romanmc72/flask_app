test:
	# linting warnings should not prevent us from moving forward.
	# also, line length of 80 is too restrictive.
	flake8 \
	--exclude docs,migrations,configs,app/__init__.py \
	--max-line-length 160 \
	--statistics \
	./
	
	# Probably should create some unit tests at some point
	# But I am not there yet...
	# cov requires pytest-cov library
	# py.test \
	# --cov=src \
	# --cov-report term-missing \
	# --cov-config=.coveragerc \
	# --verbose
