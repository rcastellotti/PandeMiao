'''Utils for connecting to the DB.'''

import logging
import time
from neo4j import GraphDatabase, Driver
from neobolt.exceptions import ServiceUnavailable
import utils.dbmigration as dbmigration
import settings


def db_connect(retry: int, wait_sec: float) -> Driver:
    '''Try to connect to the DB multiple times.'''
    db_auth = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
    try:
        db_link: Driver
        db_link = GraphDatabase.driver(settings.NEO4J_URI,
                                       auth=db_auth,
                                       encrypted=settings.NEO4J_ENCRYPTED)
        dbmigration.migrate_db(db_link)
        return db_link
    except ServiceUnavailable as exc:
        if retry == 0:
            logging.critical('DB []: Service Unavailable.')
            raise exc

        time.sleep(wait_sec)
        logging.info('DB []: Service Unavailable. Trying to reconnect...')
        return db_connect(retry-1, wait_sec)
