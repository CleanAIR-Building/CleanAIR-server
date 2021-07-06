from configparser import ConfigParser
from pathlib import Path


def config(section: str, filename: str = "./resources/clean_air_backend.ini"):
    ini = Path(filename)
    if not ini.is_file():
        raise FileNotFoundError("File {filename} does not exist!".format(filename=str(ini)))
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(ini)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise KeyError("Section {0} not found in the {1} file".format(section, filename))

    return db
