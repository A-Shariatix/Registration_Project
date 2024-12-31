import unittest
import util


class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.data = {'cat': 'meow'}
        self.user = 'cat'
        self.password = b'$2b$12$NmjU6/raMmtCvJMHgx6ht.j/eAeUzCjT0Uz3.Ey7tgX9hoP/G.P4K'

    def test_hash(self):
        self.assertEqual(util.generate_hash(self.data, self.user), self.password)

    def test_valid_input(self):
        self.assertEqual(util.check_input_data(self.data, self.user), True)

    def test_invalid_input_username_missing(self):
        self.assertEqual(util.check_input_data({'': 'meow'}, ''), False)

    def test_invalid_input_password_missing(self):
        self.assertEqual(util.check_input_data({'cat': ''}, 'cat'), False)


if __name__ == '__main__':
    unittest.main()
