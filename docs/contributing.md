<!-- contributing.md -->
# Contributing Guide

## Development Setup

1. Fork the repository
2. Create a feature branch
3. Set up development environment
4. Install dev dependencies

## Code Style

- Follow PEP 8
- Use type hints
- Write clear docstrings
- Keep functions focused

## Testing

### Adding New Tests

1. Create test file in `tests/` directory
2. Use appropriate fixtures
3. Follow existing naming conventions
4. Include docstrings
5. Update documentation

### Test Coverage

- Aim for high coverage
- Test edge cases
- Include negative tests

## Pull Request Process

1. Write tests for new features
2. Update documentation
3. Run full test suite
4. Submit PR with description

## Documentation

### Docstring Format

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description.

    Extended description if needed.

    Args:
        param1 (type): Description
        param2 (type): Description

    Returns:
        return_type: Description

    Raises:
        ExceptionType: Description
    """
```