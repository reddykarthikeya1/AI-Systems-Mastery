# Academy Top-Level Quality Gate Runner

.PHONY: test-all check-gates check-beginner check-integrity check-deps check-quizzes check-contracts client-check smoke-test

test-all: check-gates client-check smoke-test
	@echo "All repo-level quality gates passed!"

check-gates: check-contracts check-quizzes check-beginner check-integrity check-deps
	@echo "All python invariant gates passed!"

check-contracts:
	python tools/check_module_contracts.py

check-quizzes:
	python tools/check_quiz_content.py

check-beginner:
	@for d in 01_* 02_* 03_* 04_* 05_* 06_* 07_* 08_* 09_* 10_* 11_* 12_*; do \
		if [ -f "$$d/tools/check_beginner_layer.py" ]; then \
			python "$$d/tools/check_beginner_layer.py" || exit 1; \
		fi \
	done

check-integrity:
	@for d in 01_* 02_* 03_* 04_* 05_* 06_* 07_* 08_* 09_* 10_* 11_* 12_*; do \
		if [ -f "$$d/tools/check_integrity.py" ]; then \
			python "$$d/tools/check_integrity.py" || exit 1; \
		fi \
	done

check-deps:
	@for d in 01_* 02_* 03_* 04_* 05_* 06_* 07_* 08_* 09_* 10_* 11_* 12_*; do \
		if [ -f "$$d/tools/check_deps.py" ]; then \
			python "$$d/tools/check_deps.py" || exit 1; \
		fi \
	done

client-check:
	cd learning_platform/client && npm test -- --run
	cd learning_platform/client && npx tsc --noEmit
	cd learning_platform/client && npx eslint .

smoke-test:
	python tests/test_platform_smoke.py
