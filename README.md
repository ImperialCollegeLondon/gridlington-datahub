# gridlington-datahub

## Running the Server

A Dockerfile and docker-compose is provided to be able to run the server. This should be as simple as:

```bash
docker compose up
```

And the server will be available at `localhost:8000`

API docs can be seen at `localhost:8000/docs`

## Development

### Installation

1. Create a virtual environment with python 3.10 or higher: `python -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install development requirements in the virtual environment: `pip install -r requirements-dev.txt`.
4. Install pre-commit hooks: `pre-commit install`. QA can be checked with `pre-commit run --all-files` and will automatically check files before commiting them to git history.
5. Run tests: `pytest`. This will create a coverage report inside `htmlcov/`.

### Dependencies

Dependencies are managed using the [`pip-tools`] tool chain. Unpinned dependencies are specified in `pyproject.toml`. Pinned versions are then produced with: `pip-compile`.

To add/remove packages edit `pyproject.toml` and run the above command. To upgrade all existing dependencies run: `pip-compile --upgrade`.

Dependencies for developers are listed separately as optional, with the pinned versions being saved to `requirements-dev.txt` instead. `pip-tools` can also manage these dependencies by adding extra arguments, e.g.: `pip-compile --extra dev -o requirements-dev.txt`.

When dependencies are upgraded, both `requirements.txt` and `requirements-dev.txt` should be regenerated so that they are compatible with each other and then synced with your virtual environment with: `pip-sync requirements-dev.txt requirements.txt`.

Versions can be restricted from updating within the `pyproject.toml` using standard python package version specifiers, i.e. `"black<23"` or `"pip-tools!=6.12.2"`

Dependabot is configured to update dependencies as new versions become available.

[`pip-tools`]: https://pip-tools.readthedocs.io/en/latest/
