.PHONY: help verify test problems links deps lint integrity grade solve labs progress clean stress

help:
	@echo "verify      - every gate, fail-fast order"
	@echo "test        - full pytest suite (module projects + problem bank)"
	@echo "problems    - just the problem bank"
	@echo "links       - no broken links, no absolute paths"
	@echo "deps        - every third-party import declared"
	@echo "lint        - ruff"
	@echo "integrity   - the 6 pedagogical invariants"
	@echo "grade M=07  - run module 07's shipped tests against YOUR starter"
	@echo "solve M=07  - run module 07's problem bank against YOUR stubs"
	@echo "labs        - run every debug lab (all must exit 0)"
	@echo "progress    - how many problems you have solved"
	@echo "clean       - purge __pycache__"

verify: lint links deps test integrity
	@echo "ALL GATES PASSED"

test:
	python -m pytest -q

problems:
	python -m pytest Module_*/problems -q

links:
	python tools/check_links.py

deps:
	python tools/check_deps.py

lint:
	ruff check .

integrity:
	python tools/check_integrity.py

# Both of these MUST fail until you have done the work. If they pass on an
# untouched stub, the grading loop is broken - run `make integrity`.
grade:
	@cd Module_$(M)_*/starter && python -m pytest ../project_solution -q

solve:
	@cd Module_$(M)_*/problems && python -m pytest tests -q

labs:
	@for d in Module_*/debug_lab; do \
		echo "--- $$d"; \
		(cd $$d && python broken_*.py > /dev/null 2>&1 && echo "    exit 0 (correct)" \
			|| echo "    CRASHED - a lab must exit 0"); \
	done

progress:
	@echo "problems in the bank: $$(ls Module_*/problems/p*.py | wc -l)"
	@echo "still unimplemented:  $$(grep -l 'raise NotImplementedError' Module_*/problems/p*.py | wc -l)"

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +

stress:   ## differential fuzz YOUR solution against the reference: make stress M=16 P=05
	@python tools/stress_test.py --module $(M) --problem $(P) --trials $(or $(T),10000)
