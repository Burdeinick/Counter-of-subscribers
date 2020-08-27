import sys
import sqlite3
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB
from logger.log import MyLogging


super_logger = MyLogging().setup_logger('preparing_db_logger',
                                        'Application/logger/logfile_preparing.log')


class PreparDb:
    """The class for creating tables in a database."""
    def __init__(self):
        self.connect_db = ConnectionDB().conn

    def foreign_keys_on(self):
        """Allows you to use linked keys."""
        try:
            with self.connect_db:
                request = """PRAGMA foreign_keys=on"""
                self.connect_db.execute(request)
        except Exception:
            super_logger.error('Error', exc_info=True)

    def create_channel(self):
        """This method creates the 'channel' table."""
        try:
            with self.connect_db:
                request = """CREATE TABLE IF NOT EXISTS channel(
                            channel_id INTEGER PRIMARY KEY
                            AUTOINCREMENT NOT NULL,
                            title TEXT NOT NULL
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def create_groups(self):
        """This method creates the 'groups' table."""
        try:
            with self.connect_db:
                request = """CREATE TABLE IF NOT EXISTS groups(
                            groups_id INTEGER PRIMARY KEY
                            AUTOINCREMENT NOT NULL,
                            url_groups TEXT NOT NULL,
                            channel_id INTEGER NOT NULL,
                            FOREIGN KEY (channel_id)
                            REFERENCES channel(channel_id)
                            ON DELETE CASCADE,
                            UNIQUE(url_groups)
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def add_chanal(self):
        """This method fills in the 'channel' table."""
        try:
            with self.connect_db:
                request = """INSERT INTO channel(title)
                            VALUES('VK')
                          """
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def add_groups(self):
        """This method fills in the 'groups' table by default. """
        try:
            with self.connect_db:
                request = """INSERT INTO groups(channel_id, url_groups)
                            VALUES(1, 'rambler'),
                                (1, 'ramblermail'),
                                (1, 'horoscopesrambler'),
                                (1, 'championat'),
                                (1, 'championat.auto'),
                                (1, 'championat_cybersport'),
                                (1, 'livejournal'),
                                (1, 'afisha')
                          """
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def create_subscriber(self):
        """This method creates a table that
        the script will fill in once a day.

        """
        try:
            with self.connect_db:
                request = """CREATE TABLE IF NOT EXISTS subscriber(
                                subscriber_id INTEGER PRIMARY KEY
                                AUTOINCREMENT NOT NULL,
                                datetime TEXT NOT NULL,
                                size INTEGER NOT NULL,
                                groups_id INTEGER NOT NULL,
                                FOREIGN KEY (groups_id) REFERENCES
                                groups(groups_id) ON DELETE SET NULL
                            )"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)


def main():
    db = PreparDb()
    db.foreign_keys_on()
    db.create_channel()
    db.create_groups()
    db.add_chanal()
    db.add_groups()
    db.create_subscriber()


if __name__ == "__main__":
    main()
