from neo4j import Driver, BoltStatementResult

def migrate(db: Driver):
    constraints_to_keep = ['chatID', 'referrer']

    # Get constraints on the DB
    with db.session() as session:
        db_constraints: BoltStatementResult = session.run("""
                                     CALL db.constraints
                                     YIELD name
                                     """)
        all_constraints = db_constraints.value()
    
    # Create new constraints
    for constraint_to_keep in constraints_to_keep:
        if constraint_to_keep not in all_constraints:
            with db.session() as session:
                session.run(f"""
                            CREATE CONSTRAINT {constraint_to_keep}
                            ON (n:Person)
                            ASSERT n.chatID IS UNIQUE
                            """)

    # Drop unused ones
    db_constraints_to_drop = set(all_constraints) - set(constraints_to_keep)
    for constraint_name in db_constraints_to_drop:
        with db.session() as session:
            session.run('DROP CONSTRAINT $c', c=constraint_name)
