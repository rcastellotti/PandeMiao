from neo4j import Transaction, BoltStatementResult


def get_referrer(tx: Transaction, chatID: int) -> str:
    query = """
                MATCH (user:Person { chatID: $chatID })
                RETURN user.referrer
            """
    result: str = tx.run(query, chatID=chatID).single().value()
    return result


def create_node(tx: Transaction, chatID: int) -> str:
    query = """
                CREATE (newUser:Person {
                    chatID: $chatID,
                    referrer: apoc.create.uuid(),
                    infectedFromDate: date()
                })
                RETURN newUser.referrer
            """
    result: str = tx.run(query, chatID=chatID).single().value()
    return result


def create_node_from(tx: Transaction, chatID: int,
                     referrer: str) -> BoltStatementResult:
    query = """
                MATCH (infector:Person { referrer: $referrer })
                CREATE (newUser:Person {
                    chatID: $chatID,
                    referrer: apoc.create.uuid(),
                    infectedFromDate: date()
                }), (infector)-[:INFECTED]->(newUser)
                RETURN newUser.referrer
            """
    result: BoltStatementResult = tx.run(
        query, chatID=chatID, referrer=referrer)
    return result
