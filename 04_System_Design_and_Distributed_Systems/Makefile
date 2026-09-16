.PHONY: all test lint links deps notebooks integrity verify grade clean beginner

# `make verify` is the contract. If it is green, the course is sound.
all: verify

test:
	pytest -v

lint:
	ruff check .

links:
	python tools/check_links.py

deps:
	python tools/check_deps.py

# Every notebook must EXECUTE, not merely open. The deliberately-broken teaching
# cell is excluded by name; everything else runs the module's real code.
notebooks:
	python tools/check_notebooks.py

# The four pedagogical invariants: starters fail, debug labs stay unspoiled,
# solutions disclose they are in-process models, starters contain stubs.
integrity:
	python tools/check_integrity.py

# The full gate, in the order that fails fastest.
verify: lint links deps test notebooks integrity beginner
	@echo ""
	@echo "==================================================="
	@echo " ALL GATES GREEN - course is verified"
	@echo "==================================================="

# Grade your own work in one module: make grade M=09
grade:
ifndef M
	$(error usage: make grade M=09)
endif
	@cd $$(ls -d Module_$(M)_*)/starter && \
	  pytest ../project_solution/test_*.py -v

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.pytest_cache')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.ruff_cache')]"

beginner:
	@echo "--- beginner layer: every playground runs, asserts and stays in sync ---"
	python tools/check_beginner_layer.py
