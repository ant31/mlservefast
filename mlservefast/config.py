"""
Acquire runtime configuration from environment variables (etc).
"""

import os
import yaml


def logfile_path(jsonfmt=False, debug=False):
    """
    Returns the a logfileconf path following this rules:
      - conf/logging_debug_json.conf # jsonfmt=true,  debug=true
      - conf/logging_json.conf       # jsonfmt=true,  debug=false
      - conf/logging_debug.conf      # jsonfmt=false, debug=true
      - conf/logging.conf            # jsonfmt=false, debug=false
    Can be parametrized via envvars: JSONLOG=true, DEBUGLOG=true
    """
    _json = ""
    _debug = ""

    if jsonfmt or os.getenv("JSONLOG", "false").lower() == "true":
        _json = "_json"

    if debug or os.getenv("DEBUGLOG", "false").lower() == "true":
        _debug = "_debug"

    return os.path.join(MLSERVEFAST_CONF_DIR, "logging%s%s.conf" % (_debug, _json))


def getenv(name, default=None, convert=str):
    """
    Fetch variables from environment and convert to given type.

    Python's `os.getenv` returns string and requires string default.
    This allows for varying types to be interpolated from the environment.
    """

    # because os.getenv requires string default.
    internal_default = "$(none)$"
    val = os.getenv(name, internal_default)

    if val == internal_default:
        return default

    if callable(convert):
        return convert(val)

    return val


def envbool(value: str):
    return value and (value.lower() in ("1", "true"))


APP_ENVIRON = getenv("APP_ENV", "development")

MLSERVEFAST_API = getenv("MLSERVEFAST_API", "https://mlservefast.conny.dev")
MLSERVEFAST_SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
MLSERVEFAST_ROOT_DIR = os.path.abspath(os.path.join(MLSERVEFAST_SOURCE_DIR, "../"))
MLSERVEFAST_CONF_DIR = os.getenv(
    "MLSERVEFAST_CONF_DIR", os.path.join(MLSERVEFAST_ROOT_DIR, "conf/")
)
MLSERVEFAST_CONF_FILE = os.getenv("MLSERVEFAST_CONF_FILE", None)
MLSERVEFAST_DOWNLOAD_DIR = os.getenv("MLSERVEFAST_DOWNLOAD_DIR", "/tmp/mlservefast")


class MLServeFastConfig:
    """
    Class to initialize the projects settings
    """

    def __init__(self, defaults=None, confpath=None):
        self.settings = {
            "mlservefast": {
                "debug": False,
                "env": APP_ENVIRON,
                "url": MLSERVEFAST_API,
                "download_dir": MLSERVEFAST_DOWNLOAD_DIR,
            },
        }

        if defaults:
            self.load_conf(defaults)

        if confpath:
            self.load_conffile(confpath)

    @property
    def mlservefast(self):
        return self.settings["mlservefast"]

    def reload(self, confpath, inplace=False):
        if inplace:
            instance = self
            instance.load_conffile(confpath)
        else:
            instance = MLServeFastConfig(defaults=self.settings, confpath=confpath)
        return instance

    def load_conf(self, conf):
        for key, val in conf.items():
            self.settings[key].update(val)

    def load_conffile(self, confpath):
        with open(confpath, "r") as conffile:
            self.load_conf(yaml.load(conffile.read()))


GCONFIG = MLServeFastConfig(confpath=MLSERVEFAST_CONF_FILE)
