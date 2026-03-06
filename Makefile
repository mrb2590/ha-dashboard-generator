-include .env
export

.PHONY: setup
setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install ruff
	.venv/bin/pre-commit install --hook-type commit-msg
	.venv/bin/pre-commit install --hook-type pre-commit
	@printf "\033[92mSetup complete!\033[0m Run 'source .venv/bin/activate' to start.\n"

.PHONY: generate
generate:
	python3 scripts/fetch_ha_data.py
	makejinja

.PHONY: deploy
deploy: generate
	rsync -avz build/dashboards/ $(HA_SSH_USER)@$(HA_SSH_HOST):$(HA_DASHBOARD_PATH)

.PHONY: deploy-scp
deploy-scp: generate
	scp -r build/dashboards/* $(HA_SSH_USER)@$(HA_SSH_HOST):$(HA_DASHBOARD_PATH)

.PHONY: clean
clean:
	rm -rf build/

.PHONY: freeze
freeze:
	.venv/bin/pip freeze > requirements.txt
	@echo "\033[92mRequirements saved to requirements.txt!\033[0m"

.PHONY: format
format:
	.venv/bin/ruff format .
	.venv/bin/ruff check --fix .
	@echo "\033[92mCode formatted successfully!\033[0m"

.PHONY: lint
lint:
	.venv/bin/ruff check .
