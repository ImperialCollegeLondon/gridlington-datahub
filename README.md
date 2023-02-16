# gridlington-datahub

## Development

1. Install development requirements in a virtual environment: `pip install -r requirements-dev.txt `
2. Install pre-commit hooks: `pre-commit install`

Dependencies are managed using the [`pip-tools`] tool chain.

Unpinned dependencies are specified in `pyproject.toml`. Pinned versions are
then produced with:

```
pip-compile
```

To add/remove packages edit `pyproject.toml` and run the above command. To
upgrade all existing dependencies run:

```
pip-compile --upgrade
```

Dependencies for developers are listed separately as optional, with the pinned versions
being saved to `requirements-dev.txt` instead. `pip-tools` can also manage these
dependencies by adding extra arguments, e.g.:

```
pip-compile --extra dev -o requirements-dev.txt
```

When dependencies are upgraded, both `requirements.txt` and `requirements-dev.txt`
should be regenerated so that they are compatible with each other and then synced with
your virtual environment with:

```
pip-sync requirements-dev.txt requirements.txt
```

[`pip-tools`]: https://pip-tools.readthedocs.io/en/latest/
