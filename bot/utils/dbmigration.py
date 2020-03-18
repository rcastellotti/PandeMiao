def migrate(db):
    all_constraints = []
    constraints_to_keep = []
    with db.session() as session:
        db_constraints = session.run("""
                                     CALL db.constraints
                                     YIELD name
                                     """)

        for row in iter(db_constraints.single, False):
            all_constraints.append(row.value())

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
            session.run('DROP CONSTRAINT ' + constraint_name)
