# Contributing to Motadata APM Custom Instrumentation

Thank you for your interest in contributing to the Motadata APM Custom Instrumentation library! We welcome contributions from the internal engineering team to improve and extend this utility.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/motadata2025/motadata-apm-custom-instrumentation-python.git
   cd motadata-apm-custom-instrumentation-python
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip build setuptools wheel
   pip install -e .
   ```

## Coding Standards

- **Code Style:** We follow [PEP 8](https://peps.python.org/pep-0008/).
- **Type Hints:** All new code must include type hints.
- **Docstrings:** Public classes and methods must have docstrings following the Google style guide.
- **Exception Handling:** Use standard Python `Exception` class only (no custom exception classes).

## Pull Request Process

1. Create a new branch for your feature or bugfix: `feature/your-feature-name` or `fix/your-bug-fix`.
2. Ensure your code passes all linting and local tests.
3. Update `README.md` if you are adding new features or changing public APIs.
4. Submit a Pull Request describing your changes.

## Release Process

1. Update the version number in `pyproject.toml` and `src/motadata/apm/__init__.py`.
2. Build the package:
   ```bash
   python3 -m build
   ```
3. Verify the artifacts in `dist/`.

## Support

For any questions, please contact the Motadata Engineering Team at engg@motadata.com.
