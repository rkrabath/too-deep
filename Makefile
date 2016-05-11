
env: env/bin/activate /usr/lib/python2.7/dist-packages/pygame

env/bin/activate: requirements.txt
	test -d env || virtualenv env
	env/bin/pip install -Ur requirements.txt
	touch env/bin/activate

/usr/lib/python2.7/dist-packages/pygame:
	sudo apt-get install python-pygame

run: env
	./game.py
