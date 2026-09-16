.PHONY: up down up-oracle wait test test-live lint links deps clean beginner

up:
	docker compose up -d postgres mysql mongo redis cassandra dynamodb neo4j clickhouse elasticsearch qdrant

down:
	docker compose down -v

up-oracle:
	docker compose --profile oracle up -d oracle

wait:
	@echo "Waiting for core database healthchecks..."
	@docker compose ps

test:
	pytest -q

test-live:
	pytest -v -m "requires_postgres or requires_mongo or requires_redis or requires_cassandra or requires_neo4j or requires_elastic or requires_clickhouse or requires_oracle or requires_dynamo"

lint:
	ruff check .

links:
	python tools/check_links.py

deps:
	python tools/check_deps.py

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.pytest_cache')]"


# ---------------------------------------------------------------------------
# Mongo runs with --replSet so Module 11 can use change streams. A replica set
# must be initiated exactly once after the container is first created. The
# driver then connects with ?directConnection=true, which talks straight to the
# node instead of trying to resolve the internally-advertised member hostname.
# ---------------------------------------------------------------------------
init-mongo:
	docker exec databases-mongo-1 mongosh --quiet --eval 	  'try { rs.status().ok } catch(e) { rs.initiate({_id:"rs0",members:[{_id:0,host:"localhost:27017"}]}).ok }'

# Bring everything up and make it usable in one command.
bootstrap: up wait init-mongo
	@echo "all services ready - run: pytest -q"

beginner:
	@echo "--- beginner layer: every playground runs, asserts and stays in sync ---"
	python tools/check_beginner_layer.py
