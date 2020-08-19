from crontab import CronTab
 

def get_username():
    """This method returns the username from the config file."""
    with open('config.json', 'r') as config:
        json_str = config.read()
        json_str = json.loads(json_str)
    username = json_str['username']
    return (dbname, )


def main():
    """ """
    username = get_username()[0]
    my_cron = CronTab(user=f'{username}')
    job = my_cron.new(command='python3 /home/roy/writeDate.py')
    job.minute.every(1)
    
    my_cron.write()


if __name__ == "__main__":
    main()
