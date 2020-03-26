'''Drop and create constraints during migrations.'''

from neo4j import Driver, BoltStatementResult


# pylint: disable=C0116
def migrate(db_link: Driver) -> None:
    constraints_to_keep = []

    # Get constraints on the DB
    with db_link.session() as session:
        db_constraints: BoltStatementResult = session.run("""
                                     CALL db.constraints
                                     YIELD name
                                     """)
        all_constraints = db_constraints.value()

    # Create new constraints
    constraint_to_keep = 'chatID'
    if constraint_to_keep not in all_constraints:
        with db_link.session() as session:
            session.run(f"""
                        CREATE CONSTRAINT {constraint_to_keep}
                        ON (n:Person)
                        ASSERT n.chatID IS UNIQUE
                        """)
    constraints_to_keep.append(constraint_to_keep)

    constraint_to_keep = 'referrer'
    if constraint_to_keep not in all_constraints:
        with db_link.session() as session:
            session.run(f"""
                        CREATE CONSTRAINT {constraint_to_keep}
                        ON (n:Person)
                        ASSERT n.referrer IS UNIQUE
                        """)
    constraints_to_keep.append(constraint_to_keep)

    # Drop unused ones
    db_constraints_to_drop = set(all_constraints) - set(constraints_to_keep)
    for constraint_name in db_constraints_to_drop:
        with db_link.session() as session:
            session.run('DROP CONSTRAINT ' + constraint_name)
