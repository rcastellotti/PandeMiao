import settings
import logging
import time
from neo4j import GraphDatabase, Driver
from neobolt.exceptions import ServiceUnavailable
import utils.dbmigration as dbmigration


def db_connect(retry: int, wait_sec: float) -> Driver:
    db_auth = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
    try:
        db: Driver = GraphDatabase.driver(settings.NEO4J_URI,
                                          auth=db_auth,
                                          encrypted=settings.NEO4J_ENCRYPTED)
        dbmigration.migrate(db)
        return db
    except ServiceUnavailable as e:
        if retry == 0:
            logging.critical('DB []: Service Unavailable.')
            raise e

        time.sleep(wait_sec)
        logging.info(f'DB []: Service Unavailable. Trying to reconnect...')
        return db_connect(retry-1, wait_sec)
