# Contributing to Awesome Rinegade

Thank you for your interest in contributing to the Awesome Rinegade list! This document provides guidelines for contributing to this repository.

## How the List is Generated

The Awesome Rinegade list is automatically generated based on repositories starred by [0xrinegade](https://github.com/0xrinegade). The generation process involves:

1. Fetching all repositories starred by 0xrinegade using GitHub's API
2. Collecting metadata for each repository (stars, contributors, commits, etc.)
3. Categorizing repositories by language, industry, and purpose
4. Generating the README.md with the categorized list
5. Creating a knowledge graph in JSON-LD format showing relationships between repositories

## How to Contribute

### Suggesting Improvements

If you have suggestions for improving the categorization, descriptions, or overall structure of the list, please open an issue with your suggestions. Be specific about what you think could be improved and why.

### Code Contributions

If you'd like to contribute code improvements to the generation scripts, please follow these steps:

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes
4. Run the scripts to ensure they still work correctly
5. Submit a pull request with a clear description of your changes

### Adding New Features

If you'd like to suggest a new feature, please open an issue first to discuss it. This helps ensure that your time is well spent and that the feature aligns with the goals of the project.

## Development Setup

To set up the development environment:

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the scripts in the following order:
   - `python fetch_starred_repos.py`
   - `python fetch_repo_metadata.py`
   - `python generate_readme.py`
   - `python generate_knowledge_graph.py`

Alternatively, you can run the main script which orchestrates the entire process: `python main.py`

## Code Style

Please follow these guidelines for code style:

- Use PEP 8 for Python code
- Use meaningful variable and function names
- Add comments to explain complex logic
- Write docstrings for functions and modules

## License

By contributing to this repository, you agree that your contributions will be licensed under the same license as the repository.