from neo4j import Driver, Session, Transaction
from neobolt.exceptions import ConstraintError


def set_infected(driver: Driver, chatID: int, name: str) -> str:
    session: Session
    with driver.session() as session:

        def create_node(tx: Transaction, chatID: int, name: str) -> str:
            query = """
                CREATE (newUser:Person {
                    chatID: $chatID, name: $name,
                    referrer: apoc.create.uuid(), infectedFromDate: date(),
                    infectedUntil: date(
                        datetime({ epochmillis:timestamp()+1000*60*60*24*7 }))
                })
                RETURN newUser.referrer
            """
            result: str = tx.run(query, chatID=chatID,
                                 name=name).single().value()
            return result

        def get_referrer(tx: Transaction, chatID: int) -> str:
            query = """
                MATCH (user:Person { chatID: $chatID })
                RETURN user.referrer
            """
            result: str = tx.run(query, chatID=chatID).single().value()
            return result

        result: str
        try:
            result = session.write_transaction(create_node, chatID, name)
        except ConstraintError:
            # The user already exist, just return its referrer
            result = session.read_transaction(get_referrer, chatID)
        return result
