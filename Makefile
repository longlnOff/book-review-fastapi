sync-uv:
	uv sync

start-server:
	fastapi dev src

run-postgres-db:
	docker run --name my_postgres -e POSTGRES_USER=root -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:16-alpine

create-db:
	docker exec -it my_postgres createdb --username=root --owner=root bookly

drop-db:
	docker exec -it my_postgres dropdb bookly

stop-db:
	docker stop my_postgres

start-db:
	docker start my_postgres

ruff_check:
	ruff check
