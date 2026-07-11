.PHONY: install validate compile clean

install:
	python -m pip install -r requirements.txt

validate: compile
	python -m json.tool scripts/servers.json.example >/dev/null
	@test ! -f scripts/servers.json || (echo "Refusing to validate with scripts/servers.json present in the repo tree"; exit 1)

compile:
	python -m py_compile scripts/*.py

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
