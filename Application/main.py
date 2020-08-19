from scripts.logic.logic import RequestsDb
from scripts.logic.logic import Distributor


def main():
    a = RequestsDb().get_groups()
    # a = [(1, 'vk.com/rambler', 'VK')]
    b = Distributor(a)
    c = b.channel_handler()
    print(RequestsDb().TESTOVIY_ZAPROS())


if __name__ == "__main__":
    main()
