import sqlite3
import sys
sys.path.insert(0, 'Application/scripts')
from logic.logic import ConnectionDB


connect_db = ConnectionDB().conn


def drop_channal():
    """Request to drop the 'channel' table."""
    try:
        with connect_db:
            request = """DROP TABLE IF EXISTS channal"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{Error}.")

def drop_groups():
    """Request to drop the 'groups' table."""
    try:
        with connect_db:
            request = """DROP TABLE IF EXISTS groups"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{Error}.")

def drop_subscriber():
    """Request to drop the 'subscriber' table."""
    try:
        with connect_db:
            request = """DROP TABLE IF EXISTS subscriber"""
            connect_db.execute(request)

    except sqlite3.Error as error: 
        print(f"{Error}.")


def main():
    try:
        drop_channal()
        drop_groups()
        drop_subscriber()
        print("All tables have been deleted.")

    except Exception as exept:
       print(f"All of the tables were not deleted, {exept}.")  

main()
