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
