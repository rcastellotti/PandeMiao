from neo4j import Driver, Session
from neobolt.exceptions import ConstraintError


def set_infected(driver: Driver, chatID: int, name: str) -> str:
    with driver.session() as session:
        session: Session

        def create_node(tx, chatID, name):
            query = """
                CREATE (newUser:Person {
                    chatID: $chatID, name: $name,
                    referrer: apoc.create.uuid(), infectedFromDate: date(),
                    infectedUntil: date(
                        datetime({ epochmillis:timestamp()+1000*60*60*24*7 }))
                })
                RETURN newUser.referrer
            """
            return tx.run(query, chatID=chatID, name=name).single().value()

        def get_referrer(tx, chatID):
            query = """
                MATCH (user:Person { chatID: $chatID })
                RETURN user.referrer
            """
            return tx.run(query, chatID=chatID).single().value()

        try:
            return session.write_transaction(create_node, chatID, name)
        except ConstraintError:
            # The user already exist, just return its referrer
            return session.read_transaction(get_referrer, chatID)
