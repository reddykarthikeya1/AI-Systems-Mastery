.PHONY: help verify test links deps lint grade progress clean

help:
	@echo "verify    - all gates in fail-fast order"
	@echo "test      - pytest"
	@echo "links     - no broken links, no absolute paths"
	@echo "deps      - every third-party import declared"
	@echo "lint      - ruff"
	@echo "grade M=01 - run one module's tests against your starter"
	@echo "progress  - count written vs stub lessons"
	@echo "clean     - purge __pycache__"

verify: lint links deps test
	@echo "ALL GATES PASSED"

test:
	python -m pytest -q

links:
	python tools/check_links.py

deps:
	python tools/check_deps.py

lint:
	ruff check .

# Must FAIL on an untouched starter. If it passes, the grading loop is broken
# and is certifying work that was never done.
grade:
	@cd Module_$(M)_*/starter && python -m pytest ../project_solution -q

progress:
	@echo "lessons total:   $$(find . -path '*/lessons/*.md' | wc -l)"
	@echo "lessons stubbed: $$(grep -rl 'Status:.*NOT WRITTEN\|Status:.*🔴' --include=*.md . | wc -l)"

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
