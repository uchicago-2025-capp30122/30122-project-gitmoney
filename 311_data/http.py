import httpx
import re
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "_cache"
ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz1234567890%+,^=._"
IGNORED_KEYS = [
    "api_key",
    "apikey",
]

class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


def combine_url_with_params(url, params):
    """
    Use httpx.URL to create a URL joined to its parameters, suitable for use
    for cache keys.

    Parameters:
        - url: a URL with or without parameters already
        - params: a dictionary of parameters to add

    Returns:
        The URL with parameters added, for example:

        >>> combine_url_with_params(
            "https://example.com/api/",
            {"api_key": "abc", "page": 2}
        )
        "https://example.com/api/?api_key=abc&page=2"
    """
    url = httpx.URL(url)
    params = dict(url.params) | params  # merge the dictionaries
    return str(url.copy_with(params=params))


def url_to_cache_key(url: str) -> str:
    """
    Convert a URL to a cache key that can be stored on disk.

    The rules are as follows:

    1) All keys should be lower case. URLs are case-insensitive.
    2) The leading http(s):// should be removed.
    3) The remaining characters should all be in ALLOWED_CHARS.
       Any other characters should be converted to `_`.

    This lets us have unique filenames that are safe to write to disk.
    Some characters (notably `/`) would cause problems if not removed.
    """
    lower_case_url = url.lower()
    no_http = lower_case_url.replace('https://','')
    char_lst = []
    for char in no_http:
        if char in ALLOWED_CHARS:
            char_lst.append(char)
        else:
            char_lst.append('_')
    final = "".join(char_lst)
    return final

    
def cached_get(url, **kwargs) -> dict:
    """
    This function caches all GET requests it makes, by writing
    the successful responses to disk.

    When creating the cache_key this function must
    include all parameters EXCEPT those included in config.IGNORED_KEYS.

    This is to avoid writing your API key to disk hundreds of times.
    A potential security risk if someone were to see those files somehow.

    Parameters:
        url:        Base URL to visit.
        **kwargs:   Keyword-arguments that will be appended to the URL as
                    query parameters.

    Returns:
        Contents of response as text.

    Raises:
        FetchException if a non-200 response occurs.
    """
    
    # create clean arguments
    new_args = {}
    for key, value in kwargs.items():
        if key not in IGNORED_KEYS:
            new_args[key] = value
    
    # combine url and clean arguments
    full_url = combine_url_with_params(url,new_args)

    # create cache key from full url
    cache_key = url_to_cache_key(full_url)
    # make the cache directory if not already created
    CACHE_DIR.mkdir(exist_ok=True)

    # check if url already seen. If so, return cached copy of previous response
    path = CACHE_DIR / cache_key
    if path.exists():
        return path.read_text()

    # if url not in the cache, check server response. If server responds with
    # non-200, raise 'FetchException'
    else:
        actual_url = combine_url_with_params(url,kwargs)
        response = httpx.get(actual_url, follow_redirects = True)
        if response.status_code == 200:
            with open(path, "w") as f:
                f.write(response.text)
            return response.text
        else:
            raise FetchException(response)