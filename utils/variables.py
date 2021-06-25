"""Global variables.

Author: Sagar Paudel
Date : 2020-04-22
Description : This module is used as global variables.
"""

import json
import os
import inspect
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


class Variables:
    """Variables can be accessed.

    It stores variables parsed from the confguration.
    """

    def __init__(self):
        """Create objects."""
        try:
            # Creating paths
            current_dir = os.path.dirname(os.path.abspath(
                inspect.getfile(inspect.currentframe())))
            self.root_dir = os.path.dirname(current_dir)
            config_dir = os.path.join(self.root_dir, "config")

            # Configuration file path
            config_file_path = os.path.join(config_dir, "config.json")

            # Reading configuration
            with open(config_file_path, "r") as file:
                self.config = json.load(file)

            # mysql database Connection
            mysql_con_url = self.config["connection"]["mysql"]
            mysql_con_url_string = "{}://{}:{}@{}:{}/{}?charset={}".format(
                mysql_con_url['drivername'],
                mysql_con_url['username'],
                mysql_con_url['password'],
                mysql_con_url['host'],
                mysql_con_url['port'],
                mysql_con_url['database'],
                mysql_con_url['charset']
            )
            self.engine = create_engine(mysql_con_url_string)
            self.db_user = mysql_con_url["username"]

        except Exception as err:
            raise err


    def get_oracle_connection(self):
        """Create oracle database connection."""
        # oracle database connection
        oracle_con = self.config["connection"]["oracle"]
        oracle_con_url = ("{driver}://{username}:{password}@(DESCRIPTION = "
                          "(LOAD_BALANCE=on) (FAILOVER=ON) "
                          "(ADDRESS = (PROTOCOL = TCP)(HOST = {hostname})(PORT = {port})) "
                          "(CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = {SID})))")

        try:
            engine = create_engine(oracle_con_url.format(username=oracle_con['username'],
                                                         password=oracle_con['password'],
                                                         hostname=oracle_con['host'],
                                                         port=oracle_con['port'],
                                                         SID=oracle_con['sid_name'],
                                                         driver=oracle_con['drivername']))
            return engine
        except ConnectionError as err:
            raise err

    def __getitem__(self, key):
        """Get the value from key."""
        return self.config[key]

try:
    var = Variables()
except Exception as err:
    raise err
