import unittest

from .mixins import CacheTestMixin


class TestGraphCache(CacheTestMixin, unittest.TestCase):
    """ Tests for GraphCache. """

    def test_set_get(self):
        """ Test setting and getting a value in the cache. """
        # More interesting expiration
        self.time = 1

        # Non-existing keys return None
        self.assertEquals(self.c.get('test-key'), None)

        # Now set and get one
        self.c.set('test-key', 'test-value', 1)
        self.assertEquals(self.c.get('test-key'), 'test-value')
        self.assertEquals(self.c.get_expires('test-key'), 2)

    def test_set_multiple(self):
        """ Test setting and getting multiple keys in the cache. """

        self.c.set('test-key-1', 'test-value-1', 1)
        self.c.set('test-key-2', 'test-value-2', 1)

        self.assertEquals(self.c.get('test-key-1'), 'test-value-1')
        self.assertEquals(self.c.get('test-key-2'), 'test-value-2')

    def test_generate_expires(self):
        """ Test making an expiration time. """
        self.time = 1
        self.assertEquals(self.c.generate_expires(5), 6)

    def test_expires(self):
        """ Test expiration of cache. """

        self.c.set('test-key', 'test-value', 1)

        # It should still live after 1 second
        self.time = 1
        self.assertEquals(self.c.get('test-key'), 'test-value')

        # After 2 seconds, it should be gone
        self.time = 2
        self.assertEquals(self.c.get('test-key'), None)

if __name__ == '__main__':
    unittest.main()
