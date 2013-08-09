import unittest

from ..highlevel import Path, Ensemble

from .mixins import PathTestMixin


class TestPath(PathTestMixin, unittest.TestCase):
    def test_init(self):
        """ Test created Path. """
        pass


if __name__ == '__main__':
    unittest.main()
