# GitHub Workflows

This directory contains GitHub Actions workflows for the computer-control-mcp package.

## Test Workflow

The `test.yml` workflow runs on pushes to the main branch and on pull requests. It:

1. Sets up Python and installs dependencies
2. Runs the test suite
3. Builds the package
4. Verifies the built package can be installed and imported

This ensures that the package is always in a releasable state.

## Publishing Workflows

There are three publishing workflow options available:

### 1. `workflow.yml` - Main Publishing Workflow

This is the main workflow file that combines testing and publishing. It:

1. Runs on new releases or can be manually triggered
2. Runs tests before publishing
3. Uses PyPI's trusted publisher feature by default
4. Has commented code for token-based authentication if needed

This is the recommended workflow to use.

### 2. `publish.yml` - Token-based Publishing

This workflow uses a PyPI token for authentication. To use this workflow:

1. Generate a PyPI API token with upload permissions for your project
2. Add the token as a repository secret named `PYPI_TOKEN` in your GitHub repository settings
3. When you create a new release, the workflow will automatically build and publish your package to PyPI

### 3. `publish-trusted.yml` - Trusted Publisher

This workflow uses PyPI's trusted publisher feature, which is the recommended approach for GitHub Actions. To use this workflow:

1. Configure your PyPI project to use GitHub Actions as a trusted publisher
   - Go to your project on PyPI
   - Navigate to "Settings" > "Publishing" > "Add a new publisher"
   - Select GitHub Actions as the publisher type
   - Enter your GitHub username, repository name, and workflow filename (`publish-trusted.yml`)
2. Rename this file to `publish.yml` (or update your trusted publisher settings to match this filename)
3. When you create a new release, the workflow will automatically build and publish your package to PyPI

For more information on trusted publishers, see the [PyPI documentation](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
