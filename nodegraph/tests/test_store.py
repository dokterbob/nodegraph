import unittest
import tempfile

from ..store import GraphStore


class TestGraphStore(unittest.TestCase):
    """ Tests for GraphStore. """

    def test_init(self):
        """ Test creating a GraphStore. """
        s = GraphStore(name='test')

        self.assertEquals(s.name, 'test')

        # To be further implemented when Store API is somewhat stable.

    def test_hash(self):
        """ Test hashes for GraphStore. """

        s = GraphStore(name='test')
        same = GraphStore(name='test')
        other = GraphStore(name='test2')

        # Node objects equality
        self.assertEquals(same, s)
        self.assertNotEquals(other.key(), s.key())

        # Key equality
        self.assertEquals(same.key(), s.key())
        self.assertNotEquals(other.key(), s.key())

        # Hash equality
        self.assertEquals(hash(same), hash(s))
        self.assertNotEquals(hash(other), hash(s))

    def test_pickle(self):
        """ Basic test of Pickle functionality. """
        with tempfile.TemporaryFile() as f:
            s = GraphStore(name='test')
            s.save(f)
            del s

            # Rewind file pointer
            f.seek(0)

            s = GraphStore.load(f)
            self.assertEquals(s.name, 'test')


if __name__ == '__main__':
    unittest.main()
