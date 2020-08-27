import sys
import logging
import sqlite3
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB
from logger.log import MyLogging


super_logger = MyLogging().setup_logger('drop_tables_logger',
                                        'Application/logger/logfile_drop_tables.log')


class DropTableDb:
    """The class for deleting tables."""
    def __init__(self):
        self.connect_db = ConnectionDB().conn

    def drop_channal(self):
        """Request to drop the 'channel' table."""
        try:
            with self.connect_db:
                request = """DROP TABLE IF EXISTS channal"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def drop_groups(self):
        """Request to drop the 'groups' table."""
        try:
            with self.connect_db:
                request = """DROP TABLE IF EXISTS groups"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)

    def drop_subscriber(self):
        """Request to drop the 'subscriber' table."""
        try:
            with self.connect_db:
                request = """DROP TABLE IF EXISTS subscriber"""
                self.connect_db.execute(request)
                self.connect_db.commit()

        except Exception:
            super_logger.error('Error', exc_info=True)


def main():
    drop_tab = DropTableDb()
    drop_tab.drop_channal()
    drop_tab.drop_groups()
    drop_tab.drop_subscriber()


if __name__ == "__main__":
    main()
