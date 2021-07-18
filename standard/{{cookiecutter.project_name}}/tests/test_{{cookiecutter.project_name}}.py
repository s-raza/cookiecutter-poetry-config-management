import {{cookiecutter.project_name}}.config as cfg
from {{cookiecutter.project_name}} import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_env_config_key_present():
    assert hasattr(cfg, "env_config_key")
