import json
import sqlite3
import requests
from abstract_for_channel import AbstractCannel


class My_error(Exception):
    """ """
    pass

class ConnectionDB:
    """Class for connect to DB."""
    def __init__(self):
        self.dbname = self.get_config_db()[0]
        self.conn = sqlite3.connect(self.dbname)          # Подумать над созданием БД в определенной папке
        self.cursor = self.conn.cursor()

    def get_config_db(self)-> tuple:
        """The method getting informations of configuration file."""
        with open('config.json', 'r') as config:
            json_str = config.read()
            json_str = json.loads(json_str)
        dbname = json_str['Data_Base']['dbname']
        return (dbname, )


class RequestsDb:
    """Class for requests DB."""
    def __init__(self):
        self.connect_db = ConnectionDB()

    def get_groups(self)-> list:
        """ """
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
        """ """
        db_gr_id = info[0]
        size_group = info[1]

        print(db_gr_id, size_group)

        try:
            request = f"""INSERTINTOsubscriber(groups_id, size, datetime)
                            VALUES({db_gr_id}, {size_group}, CURRENT_DATE)
                       """        
            self.connect_db.conn.execute(request)
            self.connect_db.conn.commit()

        except Exception as error:                                          # TODO
            raise My_error('')

    def TESTOVIY_ZAPROS(self):
        try:
            request = f"""SELECT * FROM subscriber"""        
            self.connect_db.cursor.execute(request)
            return self.connect_db.cursor.fetchall()

        except Exception as error: 
            return (f"{error}")


class VkHandler(AbstractCannel):
    """ """
    def __init__(self, one_channel_info: tuple):
        self.one_channel_info = one_channel_info
        self.db_gr_id = self.one_channel_info[0]
        self.id_group_request = None
        self.size_group = None
        self.vk_token = None
        
    def pars_url(self):
        """ """
        url = self.one_channel_info[1]
        self.id_group_request = url.split('/')[-1]

    def pars_json_token(self):
        """The method getting informations of 'VK' token from json."""
        with open('config.json', 'r') as config:
            json_str = config.read()
            json_str = json.loads(json_str)
        self.vk_token = json_str['channel']['VK']['token']

    def get_size_group(self):
        """ """
        URL = f"https://api.vk.com/method/groups.getMembers?group_id={self.id_group_request}&v=5.122&offset=100&count=10&access_token={self.vk_token}"
        response = requests.get(URL)
        try:
            self.size_group = response.json()['response']['count']
        except KeyError:
            raise My_error('You probably have an error in the request. Please check group_id and access_token.')

    def picking_info(self) -> tuple:
        """ """
        return (self.db_gr_id, self.size_group)


class Distributor:
    """ """
    def __init__(self, db_channel_info: list):
        self.db_channel_info = db_channel_info
        self.channal = {"VK": VkHandler}

    def channel_handler(self):
        """ """
        for one_record in self.db_channel_info:
            title = one_record[2]
            try:
                try:
                    objhand = self.channal.get(title)(one_record)
                except TypeError as error:
                    raise My_error(f'{error}, к сожалению для обработки канала {title}, еще не разработан функционал.')

                objhand.pars_url()
                objhand.pars_json_token()
                objhand.get_size_group()
                to_subscr = objhand.picking_info()
                RequestsDb().write_to_subscribe(to_subscr)

            except Exception as error:
                raise My_error(f"{error}")


def main():
    # a = RequestsDb().get_groups()
    a = [(1, 'vk.com/rambler', 'VK')]
    b = Distributor(a)
    c = b.channel_handler()
    print(RequestsDb().TESTOVIY_ZAPROS())


if __name__ == "__main__":
    main()



