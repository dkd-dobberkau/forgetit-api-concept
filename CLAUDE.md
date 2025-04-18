# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run API: `uvicorn forgetit-api:app --reload` 
- Run sample client: `python sample-client.py`
- Install dependencies: `pip install -r requirements.txt`
- Type checking: `mypy *.py`
- Format code: `black *.py`

## Code Style Guidelines
- **Imports**: Organize imports by standard library, third-party packages, then local modules
- **Formatting**: Follow PEP 8 guidelines with 4-space indentation
- **Types**: Use type hints for function parameters and return values with the `typing` module
- **Models**: Define Pydantic models for data validation
- **Error Handling**: Use FastAPI's HTTPException for API errors with appropriate status codes
- **Documentation**: Include docstrings for functions describing purpose and parameters
- **Naming**: Use snake_case for variables/functions and PascalCase for classes
- **API Endpoints**: Group related endpoints and document with descriptive comments