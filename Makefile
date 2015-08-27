develop: install-requirements install-test-requirements

install-requirements:
	pip install -e .

install-test-requirements: install-requirements
	pip install "file://`pwd`#egg=easyci[tests]"

deploy:
	python setup.py register -r pypi && python setup.py sdist upload -r pypi
