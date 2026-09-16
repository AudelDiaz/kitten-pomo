.PHONY: install test lint clean

install:
	./install.sh

test:
	python3 -m py_compile kitten-pomo.py brain.py
	python3 brain.py --stats

lint:
	ruff check . 2>/dev/null || echo "ruff not installed, skipping lint"

clean:
	rm -rf __pycache__ .pytest_cache
