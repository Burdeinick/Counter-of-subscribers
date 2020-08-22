import time
import schedule
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import Distributor
from scripts.logic.logic import ConnectionDB


at_this_time = str(ConnectionDB().get_config_db()[2])


def job():
    """This method starts all logic."""
    req_grop = RequestsDb().get_groups()
    select_hand = Distributor(req_grop)
    final_action = select_hand.channel_handler()


def main():
    """This method starts executing the job script."""
    schedule.every().day.at(at_this_time).do(job) 
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
