

# run the web server
.FORCE: run
run: install
	# Activate virtual environment
	. venv/bin/activate
	# Run the web server
	python server.py

# create the python virtual environment
venv:
	python3 -m virtualenv venv

# install the requirements for the web server
.FORCE: install
install: venv
	mkdir -p data logs
	# Activate virtual environment
	. venv/bin/activate
	# Install requirements
	pip install -r requirements.txt

