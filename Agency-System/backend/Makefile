.PHONY: install dev mcp test fmt clean

PY ?= python

install:
	$(PY) -m pip install -e ".[dev]"

dev:
	AGENCY_REPO_ROOT?=$${AGENCY_REPO_ROOT:-..} $(PY) -m agency_backend

mcp:
	$(PY) -m agency_backend.mcp_server

mcp-sse:
	AGENCY_MCP_TRANSPORT=sse $(PY) -m agency_backend.mcp_server

test:
	$(PY) -m pytest -q

clean:
	rm -rf .pytest_cache **/__pycache__ build dist *.egg-info
