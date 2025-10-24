# Project Guidelines

This project follows modern Python development practices. Please adhere to the following guidelines when generating or modifying code.

## Project Structure & Design

- **Single Responsibility Principle (SRP)**: Each script should have a single, well-defined purpose. Refer to the `README.md` for the intended architecture and responsibilities of each component. Avoid long, monolithic scripts/functions.
- **Documentation**: Ensure all functions are type-hinted and have docstrings that concisely outline what they do.

## Tooling & Environment

- **Virtual Environment Location**: Virtual environment is located at `.venv\Scripts\python.exe`. Virtual environment is managed by `uv`.
- **Formatting & Linting**: Code is formatted and linted using `ruff`. Please ensure any generated code is compliant with `ruff`'s default rules and standard Python style guides (PEP 8).
- **Operating System**: The scripts are designed to run on Windows. Ensure that any file paths and commands are compatible with PowerShell.

## Testing Framework

- **Testing Library**: Use `pytest` for all testing.
- **Test Organization**: 
  - Create test files in a `tests/` directory at the project root
- **Import Handling**: 
  - Import modules using relative imports from the project root, e.g., `from src.multipatch.create_multipatch import function_name`

## General Instructions

- If asked to come up with a plan, first decide whether the task is viable in the first place. If the task doesn't make sense or is not feasible, don't be afraid to highlight that. If the task is viable, focus on a concrete and implementable plan. DO NOT proceed with code modification till the plan has been reviewed.
- DO NOT care about backwards compatibility, this project is in active development. Breakages are expected. The goal is to develop a streamlined program that abides by best practices.

## Code Quality Standards

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write clear, concise docstrings for all functions and classes
- Maintain consistent naming conventions
- Keep functions focused and avoid deep nesting
- Handle errors gracefully with appropriate exception handling
