.PHONY: setup test lint check dev clean

# Install all dependencies
setup:
	cd rag-service && uv sync

# Run all tests
test:
	cd rag-service && uv run pytest

# Run linter
lint:
	cd rag-service && uv run ruff check app/

# Type check
typecheck:
	cd rag-service && uv run mypy app/

# Full verification (test + lint)
check: test lint

# Start dev server
dev:
	cd rag-service && uv run uvicorn app.main:app --reload

# Clean temp files
clean:
	rm -rf rag-service/.tmp rag-service/pytest-cache-files-* rag-service/rag_service.egg-info
