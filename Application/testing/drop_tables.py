import sys
import logging
import sqlite3
sys.path.insert(0, 'Application')
from scripts.logic.logic import ConnectionDB
from logger.log import MyLogging


connect_db = ConnectionDB().conn
super_logger = MyLogging().setup_logger('drop_tables_logger',
                                        'Application/logger/logfile_drop_tables.log')


def drop_channal():
    """Request to drop the 'channel' table."""
    try:
        with connect_db:
            request = """DROP TABLE IF EXISTS channal"""
            connect_db.execute(request)

    except Exception:
        super_logger.error('Error', exc_info=True)


def drop_groups():
    """Request to drop the 'groups' table."""
    try:
        with connect_db:
            request = """DROP TABLE IF EXISTS groups"""
            connect_db.execute(request)

    except Exception:
        super_logger.error('Error', exc_info=True)


def drop_subscriber():
    """Request to drop the 'subscriber' table."""
    try:
        with connect_db:
            request = """DROP TABLE IF EXISTS subscriber"""
            connect_db.execute(request)

    except Exception:
        super_logger.error('Error', exc_info=True)


def main():
    drop_channal()
    drop_groups()
    drop_subscriber()


if __name__ == "__main__":
    main()
