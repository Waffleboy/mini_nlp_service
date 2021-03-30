"""
This contains all the helper methods for the api
"""

from urllib.parse import urlparse
from lxml import etree

import logging
logger = logging.getLogger(__name__)


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
    detected_xpaths = [x for x in xpaths_delimited_by_semicolon.split(
        ';') if x not in SKIP]

    try:
        [etree.XPath(x) for x in detected_xpaths]
    except Exception as e:
        logger.error(
            "xpath detection failed for xpaths {} - {}".format(detected_xpaths, e))
        return []  # failed

    return detected_xpaths
