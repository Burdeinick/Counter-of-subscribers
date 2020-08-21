import json
import sqlite3
import requests
import time 
from scripts.logic.abstract_for_channel import AbstractCannel


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
        dbname = str(json_str['Data_Base']['dbname'])
        vktok = str(json_str['channel']['VK']['token'])
        return (dbname, vktok)


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
                         FROM channel JOIN groups USING(channel_id)
                      """        
            self.connect_db.cursor.execute(request)
            return self.connect_db.cursor.fetchall()

        except Exception as error:
            print(f"{error}.")
            raise MemoryError("""This error in the 'logic.py' file 
                                  in the 'get_groups' method, the class RequestsDb.""")
    
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
            print("""{error}. This error in the 'logic.py' file 
                              in the 'write_to_subscribe' method, the class RequestsDb.""")

    def add_new_group(self, new_group:str) -> bool:
        """This method makes a query in the database by adding a new group.
           'channel_id' = 1 because the channel('VK') in the table 'channel' = 1
        """
        try:
            request = f"""INSERT INTO groups(url_groups, channel_id)
                          VALUES('{new_group}', 1)
                       """        
            self.connect_db.conn.execute(request)
            self.connect_db.conn.commit()
            return True

        except Exception as error:
            print(f"""The new group is not added, {error}. A group with this 'URL'
                      probably already exists. This error  in the 'logic.py' file 
                      in the 'add_new_group method.""")
            return False


#################################################################################################
# УДАЛИТЬ ПЕРЕД РЕЛИЗОМ!

    def TESTOVIY_ZAPROS(self):
        try:
            request = f"""SELECT subscriber_id, groups_id, datetime, url_groups, size
                          FROM groups JOIN subscriber USING(groups_id)
                       """        
            self.connect_db.cursor.execute(request)
            return self.connect_db.cursor.fetchall()

        except Exception as error: 
            return (f"{error}1111111111")
#################################################################################################

class VkHandler(AbstractCannel):
    """This class can handle 'VK' groups. 
    By API request it can to get number of users.

    """
    def __init__(self, one_channel_info: tuple):
        self.connect = ConnectionDB()
        self.one_channel_info = one_channel_info
        self.db_gr_id = int(self.one_channel_info[0])
        self.id_group_request = None
        self.size_group = None
        self.vk_token = self.connect.get_config_db()[1]
        
    def pars_url(self):
        """The method splitting string URL.
        It leaves the part that will be used in the API request in field 'group_id'.

        """
        try:
            url = str(self.one_channel_info[1])
            print('Я в парсе 1', url)
            self.id_group_request = url.split('/')[-1]
            print('Я в парсе 2', self.id_group_request)
        except Exception as error:
            print(f"""The new group is not added, {error}. A group with this 'URL'
                      probably already exists. This error  in the 'logic.py' file 
                      in the 'pars_url' method.""")



    def get_size_group(self) -> tuple:
        """This method fixate number of community members."""
        URL = f"https://api.vk.com/method/groups.getMembers?group_id={self.id_group_request}&v=5.122&offset=100&count=10&access_token={self.vk_token}"
        response = requests.get(URL)
        try:
            time.sleep(1)
            self.size_group = response.json()['response']['count']
        except Exception as error:
            print(f"""{error}. You probably have an error in the request.
                               The value of the {self.id_group_request} group is not entered in the database.
                               This error  in the 'logic.py' file in the 'get_size_group' method, the class 'VkHandler'.""")

    def picking_info(self) -> tuple:
        """This method returns a tuple that
        contains the channel id in the DB and the number of subscribers of the group.

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
            except TypeError as error:
                print(f"""{error}. Unfortunately, the functionality for processing the '{title}'
                          channel has not yet been developed.""")

            try:
                objhand.pars_url()
            except Exception as error:
                print(f"""{error}.This error in the 'logic.py' file 
                                  in the 'channel_handler' method,
                                  the class 'Distributor'. Probably 
                                  a problem with the 
                                  'objhand.pars_url()'""")
            try:
                objhand.get_size_group()
            except Exception as error:
                print(f"""{error}.This error in the 'logic.py' file 
                                  in the 'channel_handler' method,
                                  the class 'Distributor'. Probably 
                                  a problem with the 
                                  'objhand.get_size_group()'""")
            try:
                to_subscr = objhand.picking_info()
            except Exception as error:
                print(f"""{error}.This error in the 'logic.py' file 
                                  in the 'channel_handler' method,
                                  the class 'Distributor'. Probably 
                                  a problem with the 
                                  to_subscr = objhand.picking_info()'""")

            try:
                RequestsDb().write_to_subscribe(to_subscr)
            except Exception as error:
                print(f"""{error}.This error in the 'logic.py' file 
                                  in the 'channel_handler' method,
                                  the class 'Distributor'. Probably 
                                  a problem with the 
                                  'RequestsDb().write_to_subscribe(to_subscr)'""")
