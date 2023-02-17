from datahub import __version__


def test_version():
    """Check that the version is acceptable."""
    assert __version__ == "0.0.1"
