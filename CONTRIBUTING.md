# Contributing to SemanticFlow

Thank you for your interest in contributing to **SemanticFlow**! This document provides the guidelines, standards, and workflow for contributing to the compiler, persona lenses, leadership cockpit, and platform emitters.

---

## 1. Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

---

## 2. Core Architectural Invariants

Before proposing changes, ensure you understand the core design principles:

1. **Vendor Neutrality**: The Canonical Semantic AST (`src/core/ast/canonical/`) must never be contaminated with dialect-specific expressions (e.g., DAX, LookML, SQLX).
2. **Deterministic Side-Effect Free Compilation**: Running `compile()` or `project()` on the same input AST must produce byte-for-byte identical output every time.
3. **No In-Place Mutation**: Persona Lenses and the Leadership Cockpit must only read `CanonicalSemanticProject` and never mutate its state.
4. **Safe Output Invariants**: Emitters must write to isolated, temporary staging directories and atomically move on success. Writing to system root directories (`/`, `C:\`, etc.) is strictly prohibited.
5. **PII Protection**: Any attribute classified as PII must be automatically masked or filtered in consumer-facing lenses (`BUSINESS_CONSUMER`, `DATA_ANALYST`) unless explicit security overrides are granted.

---

## 3. Development Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git

### Local Environment Setup
```bash
# Clone repository
git clone https://github.com/AlvaroAlejandroFinOps/SemanticFlow.git
cd SemanticFlow

# Create virtual environment
python -m venv .venv

# Activate environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

---

## 4. Code Quality & Testing Standards

All pull requests must pass our automated quality gates:

### Linters & Type Checking
```bash
# Run Ruff linting
ruff check .

# Run Ruff formatting check
ruff format --check .

# Run Mypy static type analysis
mypy src/
```

### Running Tests & Coverage
```bash
# Run full test suite with coverage
pytest -v --cov=src --cov-branch --cov-report=term-missing

# Run golden regression tests specifically
pytest -v tests/test_golden_regression.py
```

### Test Coverage Standard
- Minimum statement coverage: **85%**
- Minimum branch coverage: **80%**
- New features or bug fixes must include corresponding unit and integration tests.

---

## 5. Development Workflow & Pull Requests

1. **Fork and Branch**: Create a feature branch from `main`:
   ```bash
   git checkout -b feat/add-new-persona-lens
   ```
2. **Implement & Test**: Write clean, typed Python code adhering to PEP 8 and project typing conventions.
3. **Commit Messages**: Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `perf:`).
4. **Pull Request**: Open a PR against `main`. Ensure CI workflows (Ubuntu, Windows, macOS across Python 3.10-3.12) pass 100%.

---

## 6. License
By contributing to SemanticFlow, you agree that your contributions will be licensed under its [Apache 2.0 License](LICENSE).
