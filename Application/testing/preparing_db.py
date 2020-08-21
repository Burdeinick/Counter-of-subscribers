import sys
import sqlite3
import logging
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB


connect_db = ConnectionDB().conn
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.ERROR):
    """The logger file 'logic.py'"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


super_logger = setup_logger('logger', 'Application/logger/logfile_preparing.log')


def foreign_keys_on():
    """Allows you to use linked keys."""
    try:
        with connect_db:
            request = """PRAGMA foreign_keys=on"""
            connect_db.execute(request)

    except sqlite3.Error:
        super_logger.error('Error', exc_info=True)


def create_channel():
    """This method creates the 'channel' table."""
    try:
        with connect_db:
            request = """CREATE TABLE IF NOT EXISTS channel(
                            channel_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            title TEXT NOT NULL
                        )"""
            connect_db.execute(request)

    except sqlite3.Error:
        super_logger.error('Error', exc_info=True)

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

    except sqlite3.Error:
        super_logger.error('Error', exc_info=True)

def add_chanal():
    """This method fills in the 'channel' table."""
    try:
        with connect_db:
            request = """INSERT INTO channel(title)
                         VALUES('VK')
                      """
            connect_db.execute(request)

    except sqlite3.Error:
        super_logger.error('Error', exc_info=True)

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

    except sqlite3.Error:
        super_logger.error('Error', exc_info=True)

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

    except sqlite3.Error:
        super_logger.error('Error', exc_info=True)


def main():
    foreign_keys_on()
    create_channel()
    create_groups()
    add_chanal()
    add_groups()
    create_subscriber()

if __name__ == "__main__":
    main()
