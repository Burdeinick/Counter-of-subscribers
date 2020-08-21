import sqlite3
import requests
import sys
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB
from scripts.logic.logic import MyError
from scripts.logic.logic import RequestsDb


class AddGroup:
    """ """
    def __init__(self):
        self.connect = ConnectionDB()
        self.request_db = RequestsDb()
        self.vk_token = self.connect.get_config_db()[1]

    def last_part_url(self, url: str) -> str:
        """ """
        return url.split('/')[-1]


    def parser_group(self, url_group: str) -> bool:
        """ """

        URL = f"https://api.vk.com/method/groups.getMembers?group_id={url_group}&v=5.122&offset=100&count=10&access_token={self.vk_token}"
        response = requests.get(URL)
        try:
            if response.json()['error']:
                return False
        except KeyError:
            return True

    def enter_new_group(self):
        """This method performs user input of a new group."""
        while True:
            inp_url_group = input("Please enter the 'URL' of the 'VK' group: ")
            last_part = self.last_part_url(inp_url_group)
            pars_gr = self.parser_group(str(last_part))
            if pars_gr:
                resp_add_new_gr = self.request_db.add_new_group(inp_url_group)
                if resp_add_new_gr:
                    print('The new group was added successfully.')
                    break
            else:
                print('Opps! There is something wrong.')
                continue


def main():
    add = AddGroup()
    check = add.enter_new_group()


main()
