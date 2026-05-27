# Contributing to mkebook

Thank you for your interest in contributing to mkebook! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or enhancements
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🧪 Write tests
- 🎨 Improve code quality

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Git

### Development Setup

1. **Fork and Clone**

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/mkebook.git
cd mkebook

# Add upstream remote
git remote add upstream https://github.com/yourusername/mkebook.git
```

2. **Set Up Environment**

```bash
# Create virtual environment with uv
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install package with development dependencies
uv pip install -e ".[dev]"
```

3. **Install Pre-commit Hooks**

```bash
pre-commit install
```

This will automatically run code quality checks before each commit.

## 🔨 Development Workflow

### 1. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clear, concise code
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mkebook --cov-report=html

# Run specific test file
pytest tests/test_core/test_ebook.py

# Run specific test
pytest tests/test_core/test_ebook.py::TestEbookCreator::test_initialization
```

### 4. Code Quality Checks

```bash
# Format code with ruff
ruff format .

# Lint code
ruff check . --fix

# Type checking with mypy
mypy src/

# Run all pre-commit hooks manually
pre-commit run --all-files
```

### 5. Commit Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new translation engine support"
```

**Commit Message Format:**

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting, etc.)
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Code Style Guidelines

### Python Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Example:

```python
from pathlib import Path
from typing import Optional

def create_ebook(
    input_file: Path,
    output_file: Path,
    title: Optional[str] = None,
) -> None:
    """Create an ebook from input file.
    
    Args:
        input_file: Path to the source file
        output_file: Path where the ebook will be saved
        title: Title of the ebook (optional)
    
    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Implementation here
    pass
```

### Documentation

- Use Google-style docstrings
- Document all public functions, classes, and methods
- Include examples in docstrings when helpful
- Keep documentation up-to-date with code changes

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

```python
def test_create_ebook_with_valid_input(sample_text_file: Path, temp_dir: Path) -> None:
    """Test creating an ebook with valid input file."""
    # Arrange
    creator = EbookCreator()
    output_file = temp_dir / "output.epub"
    
    # Act
    creator.create(
        input_file=sample_text_file,
        output_file=output_file,
        format=EbookFormat.EPUB,
    )
    
    # Assert
    assert output_file.exists()
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_core/
│   ├── __init__.py
│   ├── test_ebook.py
│   └── test_translator.py
└── test_utils.py
```

### Writing Tests

1. **Use fixtures** for common setup
2. **Test edge cases** and error conditions
3. **Mock external dependencies** (APIs, file I/O when appropriate)
4. **Keep tests independent** - each test should run in isolation

### Running Specific Tests

```bash
# Run tests in a specific file
pytest tests/test_core/test_ebook.py

# Run tests matching a pattern
pytest -k "test_create"

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x
```

## 📚 Documentation Guidelines

### Code Documentation

- Document all public APIs
- Include usage examples
- Explain complex algorithms
- Document exceptions that can be raised

### User Documentation

When adding features, update:
- `README.md` - If it affects quick start or main features
- `docs/usage.md` - For CLI usage changes
- `docs/api.md` - For API changes
- `examples/` - Add example code if helpful

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce** - Minimal steps to reproduce the issue
3. **Expected Behavior** - What you expected to happen
4. **Actual Behavior** - What actually happened
5. **Environment** - Python version, OS, package version
6. **Code Sample** - Minimal code that reproduces the issue

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
1. Step 1
2. Step 2
3. See error

**Expected Behavior**
What should happen.

**Actual Behavior**
What actually happens.

**Environment**
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.11.5]
- mkebook: [e.g., 0.1.0]

**Additional Context**
Any other relevant information.
```

## 💡 Suggesting Features

When suggesting features:

1. **Check existing issues** - Avoid duplicates
2. **Describe the use case** - Why is this feature needed?
3. **Propose a solution** - How should it work?
4. **Consider alternatives** - What other approaches exist?

## 🔍 Code Review Process

All contributions go through code review:

1. **Automated Checks** - CI/CD runs tests and linting
2. **Maintainer Review** - A maintainer reviews the code
3. **Feedback** - Address any requested changes
4. **Approval** - Once approved, the PR will be merged

### What Reviewers Look For

- Code quality and style
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations
- Backward compatibility

## 📜 License

By contributing to mkebook, you agree that your contributions will be licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 📞 Getting Help

- **Questions**: Open a [GitHub Discussion](https://github.com/yourusername/mkebook/discussions)
- **Issues**: Report bugs via [GitHub Issues](https://github.com/yourusername/mkebook/issues)
- **Chat**: Join our community chat (if available)

## 🎉 Recognition

Contributors are recognized in:
- Release notes
- Contributors list
- Project documentation

Thank you for contributing to mkebook! 🚀