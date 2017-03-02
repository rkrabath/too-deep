COVERAGE := coverage run --source entities/ --include *.py venv/bin/nose2

env: venv/bin/activate /usr/lib/python2.7/dist-packages/pygame

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --system-site-packages venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
	@echo ""
	@echo "=========="
	@echo "Please run the following command before continuing:"
	@echo "source venv/bin/activate"
	@echo "=========="

/usr/lib/python2.7/dist-packages/pygame:
	sudo apt-get install python-pygame

run: venv
	./game.py

.coverage: tests/* entities/*
	coverage run venv/bin/nose2
	coverage combine .coverage.*

test: .coverage 
	coverage report

annotate: .coverage
	coverage annotate

clean:
	rm -f .coverage .coverage.* entities/*,cover */*.pyc

.PHONY: test
