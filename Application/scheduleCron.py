import os
import json
from crontab import CronTab

 

def get_username():
    """This method returns the username from the config file."""
    with open('Application/config.json', 'r') as config:
        json_str = config.read()
        json_str = json.loads(json_str)
    username = json_str['username']
    return (username, )


def main():
    """ """
    path = os.getcwd() + '/Application/main.py'
    username = get_username()[0]
    my_cron = CronTab(user=f'{username}')

    job = my_cron.new(command=f"python3 {path}")
    job.minute.every(1)
    
    my_cron.write()
    print("Я создал новое задание")



if __name__ == "__main__":
    main()
