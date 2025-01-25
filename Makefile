WORKDIR = cafe_order
VENV = venv
MANAGE = python $(WORKDIR)/manage.py
REQS = requirements.txt

venv:
	python -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install: venv
	$(VENV)/bin/pip install -r $(REQS)
	$(VENV)/bin/$(MANAGE) migrate

run:
	$(VENV)/bin/$(MANAGE) runserver
