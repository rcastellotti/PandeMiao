def migrate(db):
    all_constraints = []
    constraints_to_keep = []
    with db.session() as session:
        db_constraints = session.run('CALL db.constraints')
        row = db_constraints.single()
        while row:
            all_constraints.append(row['name'])
            row = db_constraints.single()

    if 'chat_id' not in all_constraints:
        with db.session() as session:
            session.run("""
                        CREATE CONSTRAINT chat_id
                        ON (n:Person)
                        ASSERT n.chat_id IS UNIQUE
                        """)
    constraints_to_keep.append('chat_id')

    db_constraints_to_drop = set(all_constraints) - set(constraints_to_keep)
    for constraint_name in db_constraints_to_drop:
        with db.session() as session:
            session.run('DROP CONSTRAINT ' + constraint_name)
