import json
import sqlite3
from abstract_for_channel import AbstractCannel


class ConnectionDB:
    """Class for connect to DB."""
    def __init__(self):
        self.dbname = self.get_config_db()[0]
        self.conn = sqlite3.connect(self.dbname)          # Подумать над созданием БД в определенной папке
        self.cursor = self.conn.cursor()

        print(self.dbname)

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

    def __str__(self):
        pass

    def __repr__(self):
        pass

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


class VkHandler(AbstractCannel):
    """ """
    def __init__(self, db_channel_info: list):
        self.db_channel_info = db_channel_info

    def write_uzer_db(self):
        """Writes the number of users to the database."""
        pass



class Distributor:
    """ """
    def __itit__(self, db_channel_info: list):
        self.db_channel_info = db_channel_info
        self.channal = {"VK": VkHandler}

    def channel_selection(self):
        """ """
        for one_record in self.db_channel_info:
            title = one_record[2]
        #     if title == 'VK':
            a = self.channal.get(title)      
        return a





def main():
    a = RequestsDb()
    # print(a.get_groups())



if __name__ == "__main__":
    main()



