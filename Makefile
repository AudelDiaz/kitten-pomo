.PHONY: install test lint clean

install:
	./install.sh

test:
	PYTHONPATH=src python3 -m py_compile src/kitten_pomo/app.py src/kitten_pomo/brain.py
	XDG_STATE_HOME=/tmp/kitten-pomo-test-state PYTHONPATH=src python3 -m kitten_pomo.brain --stats

lint:
	ruff check . 2>/dev/null || echo "ruff not installed, skipping lint"

clean:
	rm -rf __pycache__ .pytest_cache
