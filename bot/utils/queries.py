'''Wrappers to interact with the DB.'''

from neo4j import Driver, Session, BoltStatementResult
from neobolt.exceptions import ConstraintError
import utils.transactions as transactions


def set_infected(driver: Driver, chat_id: int) -> str:
    '''Create a patient zero in the DB if doesn't exist.'''

    session: Session
    with driver.session() as session:
        result: str
        try:
            result = session.write_transaction(
                transactions.create_node, chat_id)
        except ConstraintError:
            # The user already exist, just return its referrer
            result = session.read_transaction(
                transactions.get_referrer, chat_id)

        return result


def set_infected_from(driver: Driver, chat_id: int, referrer: str) -> str:
    '''Create an infected in the DB if doesn't exist.'''

    session: Session
    with driver.session() as session:
        result: str
        try:
            result_st: BoltStatementResult = session.write_transaction(
                transactions.create_node_from, chat_id, referrer)

            if result_st.peek() is None:
                # If the referrer is not valid, just be the patient zero
                result = session.write_transaction(
                    transactions.create_node, chat_id)
            else:
                result = result_st.single().value()

        except ConstraintError:
            # The user already exist, just return its referrer
            result = session.read_transaction(
                transactions.get_referrer, chat_id)

        return result
