.PHONY: install test lint format run-api dashboard
install:
	uv sync --extra ai --extra quality --extra dev
test:
	uv run pytest
lint:
	uv run ruff check .
format:
	uv run black .
run-api:
	uv run uvicorn api.main:app --reload
dashboard:
	uv run streamlit run dashboard/streamlit_app.py
