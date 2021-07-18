from unittest import TestCase

import {{cookiecutter.project_name}}.config as cfg


def test_env_config_key_present():
    assert hasattr(cfg, "env_config_key")


def test_update_config_merge():

    dict_to_update = {"master_k": {"k1": "v1", "k2": {"k2.1": "val2.1"}}}

    dict_to_update_with = {"master_k": {"k3": {"k3.1": "val3.2"}}}

    updated_dict = {
        "master_k": {
            "k1": "v1",
            "k2": {"k2.1": "val2.1"},
            "k3": {"k3.1": "val3.2"},
        }
    }

    cfg.__update_config(dict_to_update, dict_to_update_with)
    TestCase().assertDictEqual(dict_to_update, updated_dict)


def test_update_config_blanks():

    dict_to_update = {}
    dict_to_update_with = {}
    updated_dict = {}

    cfg.__update_config(dict_to_update, dict_to_update_with)
    TestCase().assertDictEqual(dict_to_update, updated_dict)


def test_db_eng_str_sqlite():

    db_dict = {"sqlite": "sqlite_file.db", "db_port": 3333}
    correct = f"sqlite:///{db_dict['sqlite']}"
    assert cfg.__get_engine_string(db_dict) == correct


def test_db_eng_str_blank():

    db_dict = {}
    assert cfg.__get_engine_string(db_dict) == ""
