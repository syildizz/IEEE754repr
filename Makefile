
install:
	python3 -m pip install .

build:
	python3 -m build

remove: uninstall clean

clean:
	rm -rf build
	rm -rf src/*.egg-info
	rm -rf dist

uninstall:
	python3 -m pip uninstall ieee754repr

.PHONY : build install remove clean uninstall
