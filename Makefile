.PHONY: dcps
dcps:
	docker compose -f docker-compose.local.yaml ps

.PHONY: dcdn
dcdn:
	docker compose -f docker-compose.local.yaml down

.PHONY: dcdn-v
dcdn-v:
	docker compose -f docker-compose.local.yaml down -v

.PHONY: dcupd
dcupd:
	docker compose -f docker-compose.local.yaml up -d

.PHONY: dce-db
dce-db:
	docker compose -f docker-compose.local.yaml exec db psql

.PHONY: reset-db
reset-db:
	@echo "dcdn -v..."
	docker compose -f docker-compose.local.yaml down -v
	@echo "dcupd..."
	docker compose -f docker-compose.local.yaml up -d
	@echo "Migrating..."
	flask db upgrade

