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


    def check_status(self):
        """ """

        while True:
            url_group = input("Please enter the 'URL' of the 'VK' group: ")
            URL = f"https://api.vk.com/method/groups.getMembers?group_id={url_group}&v=5.122&offset=100&count=10&access_token={self.vk_token}"
            response = requests.get(URL)
            status = response.status_code

            if status == 200:
                resp_add_new_gr = self.request_db.add_new_group(url_group)
                if resp_add_new_gr:
                    print('The new group was added successfully.')
                    break
                else:
                    print('Новая группа не была успешно добавлена.')
                    again = input('Хотитите попробовать ввести еще раз?(ввдедите да, если хотитет)')
                    if again == 'да':
                        continue

            else:
                print('Эта группа не подает признаков жизни.')


def main():
    a = AddGroup()
    b = a.check_status()


main()
