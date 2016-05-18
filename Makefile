
env: env/bin/activate /usr/lib/python2.7/dist-packages/pygame

env/bin/activate: requirements.txt
	test -d env || virtualenv --system-site-packages env
	env/bin/pip install -Ur requirements.txt
	touch env/bin/activate
	@echo ""
	@echo "=========="
	@echo "Please run the following command before continuing:"
	@echo "source env/bin/activate"
	@echo "=========="

/usr/lib/python2.7/dist-packages/pygame:
	sudo apt-get install python-pygame

run: env
	./game.py

test:
	coverage run --source entities/ --include *.py env/bin/nose2 && coverage report


