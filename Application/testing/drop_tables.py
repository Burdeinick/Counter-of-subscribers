import sys
import logging
import sqlite3
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


super_logger = setup_logger('drop_tables_logger', 'Application/logger/logfile_drop_tables.log')


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
