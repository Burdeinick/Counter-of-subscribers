import time
import json
import sqlite3
import logging
import requests
from scripts.logic.abstract_for_channel import AbstractCannel


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.ERROR):
    """The logger file 'logic.py'"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


super_logger = setup_logger('logger', 'Application/logger/logfile_logic.log')


class ConnectionDB:
    """Class for connect to DB."""
    def __init__(self):
        self.dbname = self.get_config_db()[0]
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def get_config_db(self) -> tuple:
        """The method getting informations of configuration file."""
        with open('Application/config.json') as config:
            json_str = config.read()
            json_str = json.loads(json_str)
        dbname = str(json_str['data_Base']['dbname'])
        vktok = str(json_str['channel']['VK']['token'])
        sched = str(json_str['schedule'])
        return (dbname, vktok, sched)


class RequestsDb:
    """Class for requests DB.
    The query syntax is intended for working with the 'Sqlite' database.

    """
    def __init__(self):
        self.connect_db = ConnectionDB()

    def get_groups(self) -> list:
        """This request returns all the groups to get information from.
        For example: [(1, 'vk.com/rambler', 'VK'), ...].

        """
        try:
            request = """SELECT groups_id, url_groups, title
                         FROM channel JOIN groups USING(channel_id)
                      """
            self.connect_db.cursor.execute(request)
            return self.connect_db.cursor.fetchall()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def write_to_subscribe(self, info: tuple):
        """This request fills the database with the collected information."""
        db_gr_id = info[0]
        size_group = info[1]
        try:
            request = f"""INSERT INTO subscriber(groups_id, size, datetime)
                          VALUES({db_gr_id}, {size_group}, CURRENT_DATE)
                       """
            self.connect_db.conn.execute(request)
            self.connect_db.conn.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def add_new_group(self, new_group: str) -> bool:
        """This method makes a query in the database by adding a new group.
           'channel_id' = 1 because the channel('VK') in
           the table 'channel' = 1.

        """
        try:
            request = f"""INSERT INTO groups(url_groups, channel_id)
                          VALUES('{new_group}', 1)
                       """
            self.connect_db.conn.execute(request)
            self.connect_db.conn.commit()
            return True

        except Exception:
            super_logger.error('Error', exc_info=True)
            return False


class VkHandler(AbstractCannel):
    """This class can handle 'VK' groups.
    By API request it can to get number of users.

    """
    def __init__(self, one_channel_info: tuple):
        self.connect = ConnectionDB()
        self.one_channel_info = one_channel_info
        self.db_gr_id = int(self.one_channel_info[0])
        self.id_group_request = str(one_channel_info[1])
        self.size_group = None
        self.vk_token = self.connect.get_config_db()[1]

    def get_size_group(self) -> tuple:
        """This method fixate number of community members."""
        URL = f"https://api.vk.com/method/groups.getMembers?group_id={self.id_group_request}&v=5.122&offset=100&count=10&access_token={self.vk_token}"
        response = requests.get(URL)
        try:
            time.sleep(1)
            self.size_group = response.json()['response']['count']

        except Exception:
            super_logger.error('Error', exc_info=True)

    def picking_info(self) -> tuple:
        """This method returns a tuple that
        contains the channel id in the DB and the number of
        subscribers of the group.

        """
        return (self.db_gr_id, self.size_group)


class Distributor:
    """The channel handler class."""
    def __init__(self, db_channel_info: list):
        self.db_channel_info = db_channel_info
        self.channel = {"VK": VkHandler}

    def channel_handler(self):
        """According to which channel to process,
        this method selects an object that can do this.

        """
        for one_record in self.db_channel_info:
            title = str(one_record[2])
            try:
                objhand = self.channel.get(title)(one_record)
            except Exception:
                super_logger.error('Error', exc_info=True)

            try:
                objhand.get_size_group()
            except Exception:
                super_logger.error('Error', exc_info=True)

            try:
                to_subscr = objhand.picking_info()
            except Exception:
                super_logger.error('Error', exc_info=True)

            try:
                RequestsDb().write_to_subscribe(to_subscr)
            except Exception:
                super_logger.error('Error', exc_info=True)
