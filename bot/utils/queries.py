from neo4j import Driver, Session, BoltStatementResult
from neobolt.exceptions import ConstraintError
import utils.transactions as transactions


def set_infected(driver: Driver, chatID: int) -> str:
    session: Session
    with driver.session() as session:
        result: str
        try:
            result = session.write_transaction(
                transactions.create_node, chatID)
        except ConstraintError:
            # The user already exist, just return its referrer
            result = session.read_transaction(
                transactions.get_referrer, chatID)
        finally:
            return result


def set_infected_from(driver: Driver, chatID: int, referrer: str) -> str:
    session: Session
    with driver.session() as session:
        result: str
        try:
            result_st: BoltStatementResult = session.write_transaction(
                transactions.create_node_from, chatID, referrer)

            if result_st.peek() is None:
                # If the referrer is not valid, just be the patient zero
                result = session.write_transaction(
                    transactions.create_node, chatID)
            else:
                result = result_st.single().value()

        except ConstraintError:
            # The user already exist, just return its referrer
            result = session.read_transaction(
                transactions.get_referrer, chatID)
        finally:
            return result
