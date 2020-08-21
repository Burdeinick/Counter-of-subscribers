import time
import schedule
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import Distributor


def job():
    req_grop = RequestsDb().get_groups()
    select_hand = Distributor(req_grop)
    final_action = select_hand.channel_handler()

    for one_tup in RequestsDb().testoviy_zapros():
        print(one_tup)
        

def main():
    schedule.every().minute.at(":10").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
