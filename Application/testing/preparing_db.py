import sqlite3
import sys
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB


connect_db = ConnectionDB().conn


def foreign_keys_on():
    """ """
    try:
        with connect_db:
            request = """PRAGMA foreign_keys=on"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{error}.")


def create_channal():
    """ """
    try:
        with connect_db:
            request = """CREATE TABLE IF NOT EXISTS channal(
                            channal_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            title TEXT NOT NULL,
                            UNIQUE(title)
                        )"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{error}.")


def create_groups():
    """ """
    try:
        with connect_db:
            request = """CREATE TABLE IF NOT EXISTS groups(
                         groups_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                         url_groups TEXT NOT NULL,
                         channal_id INTEGER NOT NULL,
                         FOREIGN KEY (channal_id) REFERENCES channal(channal_id) ON DELETE CASCADE,
                         UNIQUE(url_groups)
                         )"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{error}.")

def add_chanal():
    """ """
    try:
        with connect_db:
            request = """INSERT INTO channal(title)
                         VALUES('VK')
                      """
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{error}.")

def add_groups():
    """ """
    try:
        with connect_db:
            request = """INSERT INTO groups(channal_id, url_groups)
                         VALUES(1, 'vk.com/rambler'),
                               (1,'vk.com/ramblermail'),
                               (1, 'vk.com/horoscopesrambler'),
                               (1, 'vk.com/championat'),
                               (1, 'vk.com/championat.auto'),
                               (1, 'vk.com/championat_cybersport'),
                               (1, 'vk.com/livejournal'),
                               (1, 'vk.com/afisha')
                      """
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{error}.")

def create_subscriber():
    """ """
    try:
        with connect_db:
            request = """CREATE TABLE IF NOT EXISTS subscriber( 
                            subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            datetime TEXT NOT NULL,
                            size INTEGER NOT NULL,
                            groups_id INTEGER NOT NULL,
                            FOREIGN KEY (groups_id) REFERENCES groups(groups_id) ON DELETE SET NULL
                         )"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{error}.")


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
