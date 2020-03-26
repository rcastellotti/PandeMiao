'''Wrappers to raw Cypher queries.'''

from neo4j import Transaction, BoltStatementResult


def get_infector(txn: Transaction, chat_id: int) -> str:
    '''Get chatID of the infector'''

    query = """
                MATCH (infector:Person)-[]->(:Person { chatID: $chat_id })
                RETURN infector.chatID
            """
    result: str = txn.run(query, chat_id=chat_id).single().value()
    return result


def get_referrer(txn: Transaction, chat_id: int) -> str:
    '''Get referrer of a user.'''

    query = """
                MATCH (user:Person { chatID: $chat_id })
                RETURN user.referrer
            """
    result: str = txn.run(query, chat_id=chat_id).single().value()
    return result


def create_node(thx: Transaction, chat_id: int) -> str:
    '''Create a patient zero in the DB.'''

    query = """
                CREATE (newUser:Person {
                    chatID: $chat_id,
                    referrer: apoc.create.uuid(),
                    infectedFromDate: date()
                })
                RETURN newUser.referrer
            """
    result: str = thx.run(query, chat_id=chat_id).single().value()
    return result


def create_node_from(thx: Transaction, chat_id: int,
                     referrer: str) -> BoltStatementResult:
    '''Create an infected in the DB.'''

    query = """
                MATCH (infector:Person { referrer: $referrer })
                CREATE (newUser:Person {
                    chatID: $chat_id,
                    referrer: apoc.create.uuid(),
                    infectedFromDate: date()
                }), (infector)-[:INFECTED]->(newUser)
                RETURN newUser.referrer
            """
    result: BoltStatementResult = thx.run(
        query, chat_id=chat_id, referrer=referrer)
    return result
