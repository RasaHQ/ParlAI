import unittest

import parlai.mturk.tasks.woz.backend.commands as commands


class TestCommands(unittest.TestCase):
    def test_query_constraints(self):
        query = commands.command_from_message(
            {"text": "? [{'HasBalcony': 'True'}]"}, sender=None
        )

        self.assertIsInstance(query, commands.QueryCommand)
        self.assertDictEqual(query.constraints[0], {'HasBalcony': True})

    def test_query_constraints_with_comparator(self):
        query = commands.command_from_message(
            {"text": "? [{'Floor': 'api.is_greater_than(5)'}]"}, sender=None
        )

        self.assertIsInstance(query, commands.QueryCommand)
        self.assertSetEqual(set(query.constraints[0]), {'Floor'})
        self.assertTrue(callable(query.constraints[0]["Floor"]))


if __name__ == '__main__':
    unittest.main()
