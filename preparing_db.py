import sqlite3
from logic import ConnectionDB


connect_db = ConnectionDB().conn


def foreign_keys_on():
    """ """
    try:
        with connect_db:
            request = """PRAGMA foreign_keys=on"""
            connect_db.execute(request)

    except sqlite3.IntegrityError: 
        print("...")


def create_channal():
    """ """
    try:
        with connect_db:
            request = """CREATE TABLE channal(
                            channal_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            title TEXT NOT NULL
                        )"""
            connect_db.execute(request)

    except sqlite3.IntegrityError: 
        print("couldn't create channal table")


def create_groups():
    """ """
    try:
        with connect_db:
            request = """CREATE TABLE groups(
                        groups_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        url_groups TEXT NOT NULL,
                        channal_id INTEGER NOT NULL,
                        FOREIGN KEY (channal_id) REFERENCES channal(channal_id) ON DELETE CASCADE
                        )"""
            connect_db.execute(request)

    except sqlite3.IntegrityError: 
        print("couldn't create groups table")


def add_chanal():
    """ """
    try:
        with connect_db:
            request = """INSERT INTO channal(title)
                         VALUES('VK')
                      """
            connect_db.execute(request)

    except sqlite3.IntegrityError: 
        print("couldn't add 'VK'")       

def add_groups():
    """ """
    try:
        with connect_db:
            request = """INSERT INTO groups(channal_id, url_groups)
                         VALUES(1, 'vk.com/rambler'),
                                (1,'vk.com/ramblermail')
                      """
            connect_db.execute(request)

    except sqlite3.IntegrityError: 
        print("couldn't add channals in groups ")  

def create_subscriber():
    """ """
    try:
        with connect_db:
            request = """CREATE TABLE subscriber( 
                            subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            datetime TEXT NOT NULL,
                            size INTEGER NOT NULL,
                            groups_id INTEGER NOT NULL,
                            FOREIGN KEY (groups_id) REFERENCES groups(groups_id) ON DELETE SET NULL
                         )"""
            connect_db.execute(request)

    except sqlite3.IntegrityError: 
        print("couldn't create subscriber table")  


def main():
    try:
        foreign_keys_on()
        create_channal()
        create_groups()
        add_chanal()
        add_groups()
        create_subscriber()
        print("DB is prepared.")

    except Exception as exept:
       print(f"DB is not prepared, {exept}.")  

main()