import sqlite3
import sys
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB


connect_db = ConnectionDB().conn


def foreign_keys_on():
    """Allows you to use linked keys."""
    try:
        with connect_db:
            request = """PRAGMA foreign_keys=on"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"""{error}. This error in the 'preparing_db.py' file 
                           in the 'foreign_keys_on' method.""")


def create_channel():
    """This method creates the 'channel' table."""
    try:
        with connect_db:
            request = """CREATE TABLE IF NOT EXISTS channel(
                            channel_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            title TEXT NOT NULL
                        )"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"""{error}. This error in the 'preparing_db.py' file 
                           in the 'create_channel' method.""")

def create_groups():
    """This method creates the 'groups' table."""
    try:
        with connect_db:
            request = """CREATE TABLE IF NOT EXISTS groups(
                         groups_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                         url_groups TEXT NOT NULL,
                         channel_id INTEGER NOT NULL,
                         FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE,
                         UNIQUE(url_groups)
                         )"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"""{error}. This error in the 'preparing_db.py' file 
                           in the 'create_groups' method.""")

def add_chanal():
    """This method fills in the 'channel' table."""
    try:
        with connect_db:
            request = """INSERT INTO channel(title)
                         VALUES('VK')
                      """
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"""{error}. This error in the 'preparing_db.py' file 
                           in the 'add_chanal' method.""")

def add_groups():
    """This method fills in the 'groups' table by default. """
    try:
        with connect_db:
            request = """INSERT INTO groups(channel_id, url_groups)
                         VALUES(1, 'vk.com/rambler'),
                               (1, 'vk.com/ramblermail'),
                               (1, 'vk.com/horoscopesrambler'),
                               (1, 'vk.com/championat'),
                               (1, 'vk.com/championat.auto'),
                               (1, 'vk.com/championat_cybersport'),
                               (1, 'vk.com/livejournal'),
                               (1, 'vk.com/afisha')
                      """
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"""{error}. This error in the 'preparing_db.py' file 
                           in the 'add_groups' method.""")

def create_subscriber():
    """This method creates a table that the script will fill in once a day."""
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
         print(f"""{error}. This error in the 'preparing_db.py' file 
                            in the 'create_subscriber' method.""")


def main():
    try:
        foreign_keys_on()
        create_channel()
        create_groups()
        add_chanal()
        add_groups()
        create_subscriber()
        print("DB is prepared.")

    except Exception as error:
       print(f"DB is not prepared, {error}.")  

main()
