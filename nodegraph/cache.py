from .utils import seconds


class GraphCache(object):
    """
    Cache for Graph data, emulates a simple key-value store with expiry date.

    Note: this is only a wrapper used for dependency-free testing for now.
    Warning: there might be rounding isssues considering the expiry time.
    """
    def __init__(self, timer=seconds):
        """ Set timer, emtpy cache and expires dictionaries. """

        # Allow for pluggable timer, eases testing
        self.timer = timer

        # Flush the cache
        self.flush()

    def generate_expires(self, ttl):
        """ Generate expiration time using ttl. """
        assert isinstance(ttl, int)

        seconds = self.timer()
        assert isinstance(seconds, int)

        expires = ttl + seconds

        assert isinstance(expires, int), '{0} is not an integer'.format(expires)
        return expires

    def set(self, key, value, ttl):
        """ Set a key to value with given ttl. """

        self._cache[key] = value
        self._expires[key] = self.generate_expires(ttl)

    def get_expires(self, key):
        """ Get the expiration time for a particular key or return None. """
        # Key exists?
        try:
            expires = self._expires[key]
        except KeyError:
            # Key does not exist
            assert not key in self._cache

            return None

        assert isinstance(expires, int), '{0} is not an integer'.format(expires)

        return expires

    def get(self, key):
        """
        Get the key if not expired. If expired, remove key, return None.
        """
        expires = self.get_expires(key)

        if not expires:
            # Key does not exist
            return None

        # Key expired?
        if self.timer() > expires:
            assert key in self._expires
            assert key in self._cache

            # Delete keys
            del self._expires[key]
            del self._cache[key]

            # Return None
            return None

        # Key available
        return self._cache[key]

    def flush(self):
        """ Flush the cache """

        # Key -> value store
        self._cache = {}

        # Key -> Expiry dates
        self._expires = {}


def cache_value(key):
    """
    Caching decorator using the get_ttl() method to cache values during
    a particular time.
    """
    def cache_decorator(func):
        """ Wrapper generating the decorator based on key argument. """

        def wrapper(self, *args, **kwargs):
            """ Method performing the actual caching. """
            assert hasattr(self, 'graph')
            assert hasattr(self, 'get_ttl')

            cache_key = (self, 'weight')

            # Hit cache
            cached = self.graph.store.cache.get(cache_key)
            if cached is not None:
                return cached

            # No cached value, generate value
            value = func(self, *args, **kwargs)

            # Get minimal outgoing ttl for Edges
            ttl = self.get_ttl()

            # Write to cache
            self.graph.store.cache.set(cache_key, value, ttl)

            return value

        return wrapper

    return cache_decorator

