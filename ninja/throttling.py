import hashlib
import time
from typing import Dict, List, Optional, Tuple

from django.core.cache import cache as default_cache
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest


class BaseThrottle:
    """
    Rate throttling of requests.
    """

    def allow_request(self, request: HttpRequest) -> bool:
        """
        Return `True` if the request should be allowed, `False` otherwise.
        """
        raise NotImplementedError(".allow_request() must be overridden")

    def get_ident(self, request: HttpRequest) -> Optional[str]:
        """
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present and number of proxies is > 0. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
        """
        pass

    def wait(self) -> Optional[float]:
        """
        Optionally, return a recommended number of seconds to wait before
        the next request.
        """
        pass


class SimpleRateThrottle(BaseThrottle):
    """
    A simple cache implementation, that only requires `.get_cache_key()`
    to be overridden.

    The rate (requests / seconds) is set by a `rate` attribute on the Throttle
    class.  The attribute is a string of the form 'number_of_requests/period'.

    Period should be one of: ('s', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day')

    Previous request information used for throttling is stored in the cache.
    """

    from ninja.conf import settings

    cache = default_cache
    timer = time.time
    cache_format = "throttle_%(scope)s_%(ident)s"
    scope: Optional[str] = None
    THROTTLE_RATES: Dict[str, Optional[str]] = settings.DEFAULT_THROTTLE_RATES
    _PERIODS = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 60 * 60 * 24,
        "sec": 1,
        "min": 60,
        "hour": 60 * 60,
        "day": 60 * 60 * 24,
    }

    def __init__(self, rate: Optional[str] = None):
        self.rate: Optional[str]
        if rate:
            self.rate = rate
        else:
            self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

    def get_cache_key(self, request: HttpRequest) -> Optional[str]:
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled.
        """
        raise NotImplementedError(".get_cache_key() must be overridden")

    def get_rate(self) -> Optional[str]:
        """
        Determine the string representation of the allowed request rate.
        """
        pass

    def parse_rate(self, rate: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        pass

    def allow_request(self, request: HttpRequest) -> bool:
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        pass

    def throttle_success(self) -> bool:
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        pass

    def throttle_failure(self) -> bool:
        """
        Called when a request to the API has failed due to throttling.
        """
        pass

    def wait(self) -> Optional[float]:
        """
        Returns the recommended next request time in seconds.
        """
        pass


class AnonRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a anonymous users.

    The IP address of the request will be used as the unique cache key.
    """

    scope = "anon"

    def get_cache_key(self, request: HttpRequest) -> Optional[str]:
        pass


class AuthRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.

    The string representation of request.auth object will be used as a unique cache key.
    If you use custom auth objects make sure to implement __str__ method.
    For anonymous requests, the IP address of the request will be used.
    """

    scope = "auth"

    def get_cache_key(self, request: HttpRequest) -> str:
        pass


class UserRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.

    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """

    scope = "user"

    def get_cache_key(self, request: HttpRequest) -> str:
        pass
