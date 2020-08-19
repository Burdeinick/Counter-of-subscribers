import json
import sqlite3
import requests
from scripts.logic.abstract_for_channel import AbstractCannel


class My_error(Exception):
    """For raise any errors.
    When raising errors, a description of the errors that occurred will be added.

    """
    pass

class ConnectionDB:
    """Class for connect to DB."""
    def __init__(self):
        self.dbname = self.get_config_db()[0]
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def get_config_db(self)-> tuple:
        """The method getting informations of configuration file."""
        with open ('Application/config.json') as config:
            json_str = config.read()
            json_str = json.loads(json_str)
        dbname = json_str['Data_Base']['dbname']
        return (dbname, )


class RequestsDb:
    """Class for requests DB.
    The query syntax is intended for working with the 'Sqlite' database.
    
    """
    def __init__(self):
        self.connect_db = ConnectionDB()

    def get_groups(self)-> list:
        """This request returns all the groups to get information from.
        For example: [(1, 'vk.com/rambler', 'VK'), ...].

        """
        try:
            request = """SELECT groups_id, url_groups, title
                         FROM channal JOIN groups USING(channal_id)
                         ORDER BY groups_id
                      """        
            self.connect_db.cursor.execute(request)
            return self.connect_db.cursor.fetchall()

        except Exception as exept: 
            return (f"{exept}")
    
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
        except Exception as error:
            raise My_error(f'{error}')

#################################################################################################
# УДАЛИТЬ ПЕРЕД РЕЛИЗОМ!

    def TESTOVIY_ZAPROS(self):
        try:
            request = f"""SELECT * FROM subscriber"""        
            self.connect_db.cursor.execute(request)
            return self.connect_db.cursor.fetchall()

        except Exception as error: 
            return (f"{error}")
#################################################################################################

class VkHandler(AbstractCannel):
    """This class can handle 'VK' groups. 
    By API request it can to get number of users.

    """
    def __init__(self, one_channel_info: tuple):
        self.one_channel_info = one_channel_info
        self.db_gr_id = int(self.one_channel_info[0])
        self.id_group_request = None
        self.size_group = None
        self.vk_token = None
        
    def pars_url(self):
        """The method splitting string URL.
        It leaves the part that will be used in the API request in field 'group_id'.

        """
        url = str(self.one_channel_info[1])
        self.id_group_request = url.split('/')[-1]

    def pars_json_token(self):
        """The method getting informations of from json. So far only the token."""
        with open('Application/config.json', 'r') as config:
            json_str = config.read()
            json_str = json.loads(json_str)
        self.vk_token = str(json_str['channel']['VK']['token'])

    def get_size_group(self) -> tuple:
        """This method fixate number of community members."""
        URL = f"https://api.vk.com/method/groups.getMembers?group_id={self.id_group_request}&v=5.122&offset=100&count=10&access_token={self.vk_token}"
        response = requests.get(URL)
        try:
            self.size_group = response.json()['response']['count']
        except KeyError:
            raise My_error('You probably have an error in the request. Please check group_id and access_token.')
        except Exception as error:
            raise My_error(f"{error}")

    def picking_info(self) -> tuple:
        """This method returns a tuple that
        contains the channel id in the DB and the number of subscribers of the group.

        """
        return (self.db_gr_id, self.size_group)


class Distributor:
    """Channel handler class."""
    def __init__(self, db_channel_info: list):
        self.db_channel_info = db_channel_info
        self.channal = {"VK": VkHandler}

    def channel_handler(self):
        """According to which channel to process,
        this method selects an object that can do this.

        """
        for one_record in self.db_channel_info:
            title = str(one_record[2])
            try:
                objhand = self.channal.get(title)(one_record)
            except TypeError as error:
                raise My_error(f"{error}, unfortunately, the functionality for processing the '{title}' channel has not yet been developed.")

            try:
                objhand.pars_url()
            except Exception as error:
                raise My_error(f"{error}.")

            objhand.pars_json_token()
            objhand.get_size_group()
            to_subscr = objhand.picking_info()

            try:
                RequestsDb().write_to_subscribe(to_subscr)
            except Exception as error:
                raise My_error(f"{error}. This error raise in 'RequestsDb' class in the method 'write_to_subscribe'.")
