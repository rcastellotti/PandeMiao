from neo4j import Driver, Record, BoltStatementResult

def migrate(db: Driver):
     = []
    constraints_to_keep = []
    with db.session() as session:
        db_constraints:BoltStatementResult = session.run("""
                                     CALL db.constraints
                                     YIELD name
                                     """)
        all_constraints = db_constraints.value()

    if 'chatID' not in all_constraints:
        with db.session() as session:
            session.run("""
                        CREATE CONSTRAINT chatID
                        ON (n:Person)
                        ASSERT n.chatID IS UNIQUE
                        """)
    constraints_to_keep.append('chatID')

    if 'referrer' not in all_constraints:
        with db.session() as session:
            session.run("""
                        CREATE CONSTRAINT referrer
                        ON (n:Person)
                        ASSERT n.referrer IS UNIQUE
                        """)
    constraints_to_keep.append('referrer')

    db_constraints_to_drop = set(all_constraints) - set(constraints_to_keep)
    for constraint_name in db_constraints_to_drop:
        with db.session() as session:
            session.run('DROP CONSTRAINT $c', c=constraint_name)
