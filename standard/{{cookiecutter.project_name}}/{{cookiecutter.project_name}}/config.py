import glob
import json
import os
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import quote_plus

from dotenv import dotenv_values, load_dotenv

load_dotenv()


def __get_engine_string(database: Dict[str, Any]) -> str:

    sqlite_file = database.get("sqlite")

    if sqlite_file:
        retval = "sqlite:///{}".format(sqlite_file)

    else:

        retval = (
            database["dialect"]
            + "://"
            + database["user"]
            + ":"
            + quote_plus(database["password"])
            + "@"
            + database["host"]
        )

        if database["db_port"] is not None:
            retval = retval + ":" + database["db_port"]

        retval = retval + "/" + database["db_name"]

        if database["db_options"] is not None:

            retval = retval + "?"

            for opt, val in database["db_options"].items():
                retval = retval + opt + "=" + val + "&"

    return retval


def __get_json_config_files(dir: str) -> List[str]:

    curr_dir = os.path.join(".", dir)

    if Path(curr_dir).is_dir() is False:
        config_dir = os.path.join(".", "{{cookiecutter.project_name}}", dir)
    else:
        config_dir = f"{curr_dir}"

    config_dir = f"{config_dir}/"
    json_filter = os.path.join(config_dir, "**", "*.json")

    return [f for f in glob.glob(json_filter, recursive=True)]


def __get_dot_env_dict(
    dotenv: Dict[str, Any], env_config_key: str
) -> Dict[str, Any]:

    ret_dict = {}

    for key, val in dotenv.items():

        if key.startswith(env_config_key):

            applied_key = key.split(env_config_key)[1]

            try:
                ret_dict[applied_key] = json.loads(val)
            except json.decoder.JSONDecodeError:
                ret_dict[applied_key] = val

    return ret_dict


def __update_config(
    dict_to_update: Dict[str, Any], config_dict: Dict[str, Any]
) -> None:

    for config_key, settings in config_dict.items():

        if config_key in dict_to_update:
            dict_to_update[config_key].update(settings)
        else:
            dict_to_update[config_key] = settings


def __get_db_cfg_dict(all_cfg: Dict[str, Any]) -> Dict[str, Any]:

    db_cfg_dict: Dict[str, Any] = {}

    if all_cfg.get("active_database") is not None:
        db_cfg_dict["database"] = all_cfg[all_cfg["active_database"]]
        db_cfg_dict["database"]["conn_string"] = __get_engine_string(
            db_cfg_dict["database"]
        )
    else:
        all_cfg["database"] = None

    return db_cfg_dict


def __get_env_cfg_dict(json_cfg_dict: Dict[str, Any]) -> Dict[str, Any]:

    env_config_key = json_cfg_dict.get("env_config_key")

    if env_config_key is not None:
        dotenv_path = json_cfg_dict.get("dotenv_file_path")
        dotenv = dotenv_values(dotenv_path)
        dotenv_cfg_dict = __get_dot_env_dict(
            dotenv, env_config_key=env_config_key
        )
    else:
        dotenv_cfg_dict = {}

    return dotenv_cfg_dict


def __get_json_cfg_dict(cfg_dir: str) -> Dict[str, Any]:

    config_files_list = __get_json_config_files(cfg_dir)
    json_config: Dict[str, Any] = {}

    for f in config_files_list:

        with open(f) as file_data:
            try:
                json_cfg_file_dict = json.load(file_data)
            except json.decoder.JSONDecodeError:
                json_cfg_file_dict = {}
            __update_config(json_config, json_cfg_file_dict)

    return json_config


def __get_all_settings(cfg_dir: str = "config") -> Dict[str, Any]:

    all_cfg: Dict[str, Any] = {}

    json_cfg_dict = __get_json_cfg_dict(cfg_dir)
    __update_config(all_cfg, json_cfg_dict)

    env_cfg_dict = __get_env_cfg_dict(json_cfg_dict)
    __update_config(all_cfg, env_cfg_dict)

    db_cfg_dict = __get_db_cfg_dict(all_cfg)
    __update_config(all_cfg, db_cfg_dict)

    return all_cfg


globals().update(__get_all_settings())
