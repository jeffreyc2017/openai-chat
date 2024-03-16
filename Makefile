VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

## install the requirements
$(VENV)/bin/activate: requirements.txt
	@python3 -m venv $(VENV)
	@echo -e "\033[32m===# Install the requirements\033[0m"
	@$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

run: $(VENV)/bin/activate
	@$(PYTHON) src/main.py

test: $(VENV)/bin/activate
	@$(PYTHON) -m unittest discover -s tests

## Clean all the venv content, so you could restart the building from a clean environment
clean:
	rm -fr venv
	rm -fr src/__pycache__
	rm -fr tests/__pycache__
