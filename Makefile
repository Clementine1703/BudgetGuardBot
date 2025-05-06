# Makefile for BudgetGuardBot PostgreSQL container with .env support

.PHONY: start stop restart status logs clean connect help

# Include environment variables
include .env
export $(shell sed 's/=.*//' .env)

# Default values if not set in .env
CONTAINER_NAME = BudgetGuardBot
POSTGRES_IMAGE = postgres:16.1-bullseye
PG_PORT ?= 5432
PG_USERNAME ?= user
PG_PASSWORD ?= password
PG_DB_NAME ?= main

start:
	@echo "Starting PostgreSQL container..."
	docker run -d \
		--name $(CONTAINER_NAME) \
		-e POSTGRES_USER=$(PG_USERNAME) \
		-e POSTGRES_PASSWORD=$(PG_PASSWORD) \
		-e POSTGRES_DB=$(PG_DB_NAME) \
		-p $(PG_PORT):5432 \
		-v pg_data:/var/lib/postgresql/data \
		$(POSTGRES_IMAGE)
	@echo "PostgreSQL container started successfully"
	@echo "  Host: localhost:$(PG_PORT)"
	@echo "  User: $(PG_USERNAME)"
	@echo "  DB: $(PG_DB_NAME)"

stop:
	@echo "Stopping PostgreSQL container..."
	@docker stop $(CONTAINER_NAME) || true
	@echo "PostgreSQL container stopped"

restart: stop start
	@echo "PostgreSQL container restarted"

status:
	@docker ps -a --filter "name=$(CONTAINER_NAME)"

logs:
	@docker logs -f $(CONTAINER_NAME)

clean: stop
	@echo "Removing PostgreSQL container..."
	@docker rm $(CONTAINER_NAME) || true
	@docker volume rm pg_data || true
	@echo "Container and volume removed"

connect:
	@echo "Connecting to PostgreSQL..."
	@docker exec -it $(CONTAINER_NAME) psql -U $(PG_USERNAME) -d $(PG_DB_NAME)

help:
	@echo "Available commands:"
	@echo "  make start    - Start the PostgreSQL container"
	@echo "  make stop     - Stop the container"
	@echo "  make restart  - Restart the container"
	@echo "  make status   - Show container status"
	@echo "  make logs     - Show container logs"
	@echo "  make clean    - Remove the container and volume"
	@echo "  make connect  - Connect to PostgreSQL with psql"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Configuration is loaded from .env file"