import unittest
from utils.dbinit import db_connect
import utils.queries
from neo4j import Driver


class TestQueries(unittest.TestCase):
    db: Driver

    def setUp(self):
        self.db = db_connect(retry=5, wait_sec=5)

    def test_set_infected(self):
        # Creation of a node
        referrer = utils.queries.set_infected(self.db, 0)
        self.assertIsNotNone(referrer)

        # If a node exist, just return it
        referrer_eq = utils.queries.set_infected(self.db, 0)
        self.assertIsNotNone(referrer_eq)
        self.assertEqual(referrer, referrer_eq)

        # Different nodes have different referrer links
        referrer_diff = utils.queries.set_infected(self.db, 1)
        self.assertIsNotNone(referrer_diff)
        self.assertNotEqual(referrer, referrer_diff)

    def test_set_infected_from(self):
        # Creation of the patient zero
        patient_zero_referrer = utils.queries.set_infected(self.db, 0)
        self.assertIsNotNone(patient_zero_referrer)

        # Patient zero -> patient 1
        referred_infected = utils.queries.set_infected_from(
            self.db, 1, patient_zero_referrer)
        self.assertIsNotNone(referred_infected)
        self.assertNotEqual(patient_zero_referrer, referred_infected)

        # If a node exist, just return it
        referred_eq = utils.queries.set_infected_from(
            self.db, 1, 'no_matter_the_referral')
        self.assertIsNotNone(referred_eq)
        self.assertEqual(referred_infected, referred_eq)

        # If the referral is wrong, create a patient zero
        wrong_referral = utils.queries.set_infected_from(
            self.db, 2, 'wrong_referral')
        self.assertIsNotNone(wrong_referral)

        # If a node exist and we try to re-infect it, nothing happens
        wrong_linked = utils.queries.set_infected_from(
            self.db, 2, patient_zero_referrer)
        self.assertIsNotNone(wrong_linked)
        self.assertEqual(wrong_referral, wrong_linked)

        # If a node exist, it is a patient zero and we try to infect it, nothing happens
        no_referred = utils.queries.set_infected(self.db, 1)
        self.assertIsNotNone(no_referred)
        self.assertEqual(referred_infected, no_referred)

    def tearDown(self):
        with self.db.session() as session:
            # Clean the DB
            session.run("""
                            MATCH (n)
                            DETACH DELETE (n)
                        """)
        self.db.close()


if __name__ == '__main__':
    unittest.main()