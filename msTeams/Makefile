# Specify desired python version
BASE_PYTHON?=python3
TM_VENV?=tm_venv

PYTHON=${TM_VENV}/bin/$(BASE_PYTHON)

# .PHONY defines parts of the makefile that are not dependent on any specific file.
# This is most often used to store functions
.PHONY=help setup venv run clean

SOURCE=app.py

help:
	@echo "------------------------SELEMANDER-MSTEAMS--------------------------"
	@echo "Selemander for MSTeams allows you to automate logging in and joining"
	@echo "meetings. Just setup the project and type 'make run' to login and"
	@echo "search for meetings, or deploy the project on a remote VM and CRON"
	@echo "the script to check for meetings at regular intervals."
	@echo ""
	@echo "To setup the project type 'make setup'"
	@echo "To run the app type 'make run'"
	@echo "To clean(delete) the venv type 'make clean'"
	@echo "--------------------------------------------------------------------"

venv: $(TM_VENV)/bin/activate

setup:
	@echo "=================Installing development environment================="
	test -d $(TM_VENV) || $(BASE_PYTHON) -m venv $(TM_VENV)
	$(PYTHON) -m pip install -U pip && $(PYTHON) -m pip install -r requirements.txt && touch $(TM_VENV)/bin/activate	

run:
	@echo "==========================Running app.py============================"
	(. ${TM_VENV}/bin/activate;)
	$(PYTHON) $(SOURCE) .

clean:
	@echo "==========================Cleaning venv============================="
	rm -rf $(TM_VENV)
	find -iname "*.pyc" -delete
