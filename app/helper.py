"""
This contains all the helper methods for the api
"""

from urllib.parse import urlparse


def valid_url(url: str) -> bool:
    """Acid test for whether an input string is a valid url

    Args:
        url (str): the input url

    Returns:
        bool: True if valid url, else False
    """
    res = urlparse(url)
    return all([res.scheme, res.netloc])


def validate_and_combine_xpaths(xpaths_delimited_by_semicolon: str) -> list:
    """Simple validator for the input xpaths

    Args:
        xpaths_delimited_by_semicolon (str): as many xpaths delimited by semicolon.

    Returns:
        list: list of parsed xpaths
    """
    SKIP = {'', ' '}
    # TODO: Do more proper validation
    xpaths = [x for x in xpaths_delimited_by_semicolon.split(
        ';') if x not in SKIP]
    return xpaths
