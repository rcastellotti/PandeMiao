'''Test module utils.queries.'''

import unittest
from neo4j import Driver
from utils.dbinit import db_connect
import utils.queries


class TestQuery(unittest.TestCase):
    '''Base class for testing a query.'''

    __test__ = False  # Don't have to be run
    db_link: Driver

    def setUp(self) -> None:
        '''Connect to the DB.'''

        self.db_link = db_connect(retry=5, wait_sec=5)

    def tearDown(self) -> None:
        '''Delete all data from the DB.'''

        with self.db_link.session() as session:
            # Clean the DB
            session.run("""
                            MATCH (n)
                            DETACH DELETE (n)
                        """)
        self.db_link.close()


class TestSetInfectedFrom(TestQuery):
    '''Test the utils.queries.set_infected method.'''

    __test__ = True

    def test_new_node_referrer(self) -> None:
        '''Test creation of a new node.'''

        referrer = utils.queries.set_infected(self.db_link, 0)
        self.assertIsNotNone(referrer)

    def test_recreate_node(self) -> None:
        '''Test re-creation of a node.'''

        old_ref = utils.queries.set_infected(self.db_link, 0)
        new_ref = utils.queries.set_infected(self.db_link, 0)
        self.assertEqual(new_ref, old_ref)

    def test_unique_referrer(self) -> None:
        '''Test uniqueness of referrals.'''

        old_ref = utils.queries.set_infected(self.db_link, 0)
        self.assertIsNotNone(old_ref)

        new_ref = utils.queries.set_infected(self.db_link, 1)
        self.assertIsNotNone(new_ref)

        self.assertNotEqual(new_ref, old_ref)


class TestSetInfected(TestQuery):
    '''Test the utils.queries.set_infected_from method.'''

    __test__ = True
    patient0_chat_id = 0
    patient0_ref: str

    def setUp(self) -> None:
        '''Create a patient zero.'''

        super().setUp()
        self.patient0_ref = utils.queries.set_infected(
            self.db_link, self.patient0_chat_id)

    def test_new_node_referrer(self) -> None:
        '''Test creation of a new node.'''

        infected_ref = utils.queries.set_infected_from(
            self.db_link, 1, self.patient0_ref)
        self.assertIsNotNone(infected_ref)
        self.assertNotEqual(infected_ref, self.patient0_ref)

    def test_recreate_node(self) -> None:
        '''Test re-creation of a node.'''

        # If they are both infected from someone
        old_ref = utils.queries.set_infected_from(
            self.db_link, 1, self.patient0_ref)
        new_ref = utils.queries.set_infected_from(
            self.db_link, 1, self.patient0_ref)
        self.assertEqual(new_ref, old_ref)

        # If the first is a patient zero
        old_ref = utils.queries.set_infected(self.db_link, 1)
        new_ref = utils.queries.set_infected_from(
            self.db_link, 1, self.patient0_ref)
        self.assertEqual(new_ref, old_ref)

        # If the second is a patient zero
        old_ref = utils.queries.set_infected_from(
            self.db_link, 1, self.patient0_ref)
        new_ref = utils.queries.set_infected(self.db_link, 1)
        self.assertEqual(new_ref, old_ref)

    def test_unique_referrer(self) -> None:
        '''Test uniqueness of referrals.'''

        old_ref = utils.queries.set_infected_from(
            self.db_link, 1, self.patient0_ref)
        self.assertIsNotNone(old_ref)

        new_ref = utils.queries.set_infected_from(
            self.db_link, 2, self.patient0_ref)
        self.assertIsNotNone(new_ref)
        self.assertNotEqual(new_ref, old_ref, self.patient0_ref)

    def test_wrong_referrer(self) -> None:
        '''Test when the referrer is wrong.'''

        # If the referral is wrong, create a patient zero
        referrer = utils.queries.set_infected_from(
            self.db_link, 1, 'wrong_referral')
        self.assertIsNotNone(referrer)

        with self.db_link.session() as session:
            # It shouldn't have an infector
            self.assertRaises(AttributeError, session.read_transaction,
                              utils.transactions.get_infector, 1)

    def change_referrer(self) -> None:
        '''Test if the infector change after re-creation of a node'''
        # If a node exist and we try to re-infect it,
        # it shouldn't change the infector

        ref_init = utils.queries.set_infected(self.db_link, 1)
        utils.queries.set_infected_from(self.db_link, 3, ref_init)

        ref_post = utils.queries.set_infected(self.db_link, 2)
        utils.queries.set_infected_from(self.db_link, 3, ref_post)

        with self.db_link.session() as session:
            result = session.read_transaction(
                utils.transactions.get_infector, 3)
        self.assertEqual(result, 1)
        self.assertNotEqual(result, 2)
