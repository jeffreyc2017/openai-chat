VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

## install the requirements
$(VENV)/bin/activate: requirements.txt
	@python3 -m venv $(VENV)
	@echo -e "\033[32m===# Install the requirements\033[0m"
	@$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

run: $(VENV)/bin/activate
	@$(PYTHON) src/main.py

test: $(VENV)/bin/activate
	@$(PYTHON) -m unittest tests/test_chat_handler.py
	@$(PYTHON) -m unittest tests/test_model_selector.py
	@$(PYTHON) -m unittest tests/test_prompt_creator.py
	@$(PYTHON) -m unittest tests/test_token_counter.py

## Clean all the venv content, so you could restart the building from a clean environment
clean:
	rm -fr venv
