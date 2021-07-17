import glob
import json
import os
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

    config_dir = f"{dir}/"
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


def __load_config_dir(conf_dir: str = "./config") -> None:

    config_files_list = __get_json_config_files(conf_dir)
    all_config: Dict[str, Any] = {}
    dotenv_path: Any = ""

    for f in config_files_list:

        with open(f) as file_data:

            json_cfg_dict = json.load(file_data)
            __update_config(all_config, json_cfg_dict)

    dotenv_path = all_config.get("dotenv_file_path")
    dotenv = dotenv_values(dotenv_path)
    dotenv_cfg_dict = __get_dot_env_dict(
        dotenv, env_config_key=all_config["env_config_key"]
    )

    __update_config(all_config, dotenv_cfg_dict)

    if all_config.get("active_database") is not None:
        all_config["database"] = all_config[all_config["active_database"]]
        all_config["database"]["conn_string"] = __get_engine_string(
            all_config["database"]
        )
    else:
        all_config["database"] = None

    globals().update(all_config)


__load_config_dir()
