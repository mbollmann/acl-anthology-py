_default:
  @just -l

# ALIASES

[private]
alias t := test-all

[private]
alias ft := fix-and-test

# Install the project dependencies, but quietly
# (to be used as a dependency for all other recipes)
_deps:
  @make -s dependencies

# Install the project dependencies
install:
  make dependencies

# Install the pre-commit hooks
install-hooks: _deps
  poetry run pre-commit install

# Run checks (hooks & type-checker)
check: _deps && typecheck
  poetry run pre-commit run --all-files

# Run checks (twice in case of failure) and all tests
fix-and-test: _deps && test-all
  @poetry run pre-commit run -a || poetry run pre-commit run -a

# Run all tests
test-all: _deps
  poetry run pytest

# Run all tests and generate coverage report
test-with-coverage: _deps
  poetry run pytest --cov=acl_anthology --cov-report=xml

# Run only test functions containing TERM
test TERM: _deps
  poetry run pytest -v -k _{{TERM}}

# Run type-checker only
typecheck: _deps
  poetry run mypy acl_anthology

# TODO: clean
# TODO: docs
# TODO: test-all-python-versions
