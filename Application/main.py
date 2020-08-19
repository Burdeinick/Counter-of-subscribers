# import schedule
# import time
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import Distributor


def main():
    a = RequestsDb().get_groups()
    b = Distributor(a)
    c = b.channel_handler()
    print(RequestsDb().TESTOVIY_ZAPROS())
        
# def main():
#     schedule.every().minute.at(":17").do(job)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


main()


# if __name__ == "__main__":
#     main()
