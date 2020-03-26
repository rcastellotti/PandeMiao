'''Test module utils.queries.'''

# pylint: disable=C0116
# pylint: disable=C0115

import unittest
from neo4j import Driver
from utils.dbinit import db_connect
import utils.transactions
import utils.queries


class TestQueries(unittest.TestCase):
    db_link: Driver

    def setUp(self) -> None:
        self.db_link = db_connect(retry=5, wait_sec=5)

    def test_set_infected(self) -> None:
        # Creation of a node
        referrer = utils.queries.set_infected(self.db_link, 0)
        self.assertIsNotNone(referrer)

        # If a node exist, just return it
        referrer_eq = utils.queries.set_infected(self.db_link, 0)
        self.assertIsNotNone(referrer_eq)
        self.assertEqual(referrer, referrer_eq)

        # Different nodes have different referrer links
        referrer_diff = utils.queries.set_infected(self.db_link, 1)
        self.assertIsNotNone(referrer_diff)
        self.assertNotEqual(referrer, referrer_diff)

    def test_set_infected_from(self) -> None:
        # Creation of the patient zero
        patient_zero_referrer = utils.queries.set_infected(self.db_link, 0)
        self.assertIsNotNone(patient_zero_referrer)

        # Patient zero -> patient 1
        referred_infected = utils.queries.set_infected_from(
            self.db_link, 1, patient_zero_referrer)
        self.assertIsNotNone(referred_infected)
        self.assertNotEqual(patient_zero_referrer, referred_infected)

        # If a node exist, just return it
        referred_eq = utils.queries.set_infected_from(
            self.db_link, 1, 'no_matter_the_referral')
        self.assertIsNotNone(referred_eq)
        self.assertEqual(referred_infected, referred_eq)

        # If the referral is wrong, create a patient zero
        wrong_referral = utils.queries.set_infected_from(
            self.db_link, 2, 'wrong_referral')
        self.assertIsNotNone(wrong_referral)

        # If a node exist and we try to re-infect it, nothing happens
        wrong_linked = utils.queries.set_infected_from(
            self.db_link, 2, patient_zero_referrer)
        self.assertIsNotNone(wrong_linked)
        self.assertEqual(wrong_referral, wrong_linked)

        # If a node exist and we try to re-infect it,
        # it souldn't change the infector
        ref_init = utils.queries.set_infected(self.db_link, 3)
        ref_post = utils.queries.set_infected(self.db_link, 4)
        utils.queries.set_infected_from(self.db_link, 5, ref_init)
        utils.queries.set_infected_from(self.db_link, 5, ref_post)
        with self.db_link.session() as session:
            result = session.read_transaction(
                utils.transactions.get_infector, 5)
        self.assertEqual(result, 3)
        self.assertNotEqual(result, 4)

        # If a node exist, it is a patient zero
        # and we try to infect it, nothing happens
        no_referred = utils.queries.set_infected(self.db_link, 1)
        self.assertIsNotNone(no_referred)
        self.assertEqual(referred_infected, no_referred)

    def tearDown(self) -> None:
        with self.db_link.session() as session:
            # Clean the DB
            session.run("""
                            MATCH (n)
                            DETACH DELETE (n)
                        """)
        self.db_link.close()


if __name__ == '__main__':
    unittest.main()
