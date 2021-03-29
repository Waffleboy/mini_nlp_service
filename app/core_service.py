import bs4
from bs4 import BeautifulSoup
import requests
from typing import Type, Callable
import db_wrapper
from nlp_wrappers.nlp_wrappers import SpacyNLP
import logging
logger = logging.getLogger(__name__)
nlp_library = SpacyNLP()

# Website specific tags to pick portions of the selected website - TODO
CUSTOM_URL_PROCESSORS = {}

# in the form of {"url": list of XPATHs to target}
# eg: CUSTOM_URL_PROCESSORS = {'https://careers.gic.com.sg/job/Singapore-Associate%2C-Machine-Learning-Engineer/638994801/':["//*[@id="content"]/div/div[2]/div/div[1]/div[2]/div[8]/div/div/div"]


def run(urls: list) -> list:
    """Main method that runs the scraping pipeline on a url.
    Accepts string inputs as well

    Args:
        urls (list): List of urls to scrape. Converts single input to a string

    Returns:
        [type]: [description]
    """
    logger.debug("Running scraping for urls {}".format(urls))
    # for future, handle multi url stuff though its one by one now
    if type(urls) == str:
        urls = [urls]

    success_results = []
    for url in urls:
        logger.debug("Running scraping for url {}".format(url))
        # determine url type and get handler for it.
        handler = determine_input_handler_for_url(url)
        res = handler(url)
        list_of_entities = nlp_library.extract_entities(res)

        logger.debug("list of entities detected: {}".format(list_of_entities))
        success = db_wrapper.store_entity_results(list_of_entities, url)
        logger.debug("Db result: {}".format(success))
        success_results.append(success)
    return success_results


# =============================================================================
# Handlers (to abstract out)
# =============================================================================
"""Add handlers here for different filetypes"""


def website_handler(url: str) -> str:
    soup = scrape_link(url)
    # TODO: add custom preprocessor handling for selected urls (select certain sections etc)
    if url in CUSTOM_URL_PROCESSORS:
        # extract targeted sections via xpath and piece them together
        raise NotImplementedError

    else:
        # default behavior
        tags = extract_body_tags(soup)
    filtered_text = run_preprocessors(tags)
    return filtered_text


def csv_handler(url: str) -> str:
    raise NotImplementedError


# =============================================================================
# Helpers (to abstract out)
# =============================================================================

def determine_input_handler_for_url(url: str) -> Callable[[str], str]:
    """Returns the correct handler for a url given the filetype

    Args:
        url (str): url to scrape

    Returns:
        [function]: returns hte specific handler for the file type
    """
    MAPPER = {'.csv': csv_handler}
    for entry in MAPPER:
        if entry in url:
            return MAPPER[entry]
    return website_handler


def scrape_link(url: str) -> Type[BeautifulSoup]:
    """This downloads the current url and converts it into
    a BeautifulSoup obj to be parsed.

    Args:
        url (str): url to scrape

    Returns:
        Type[BeautifulSoup]: bs4 object
    """
    ob = requests.get(url,
                      headers=generate_headers())
    html_page = ob.content
    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


def extract_tag_by_xpath(soup: bs4.BeautifulSoup, xpath):
    raise NotImplementedError


def extract_body_tags(soup: bs4.BeautifulSoup) -> Type[bs4.element.ResultSet]:
    """Extracts the body from the given soup object, runs
    a preprocessor and returns the cleaned text

    Args:
        soup ([BeautifulSoup]): bs4 object

    Returns:
        str: cleaned body text
    """
    body = soup.find('body')
    relevant_text_tags = body.find_all(text=True)
    return relevant_text_tags


def generate_headers() -> dict:
    """Optional implementation to add custom headers to avoid
    detection by scripts. Default, static user agent

    Returns:
        dict: Headers
    """
    return {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# =============================================================================
# Text Preprocessors (to abstract out)
# =============================================================================


def run_preprocessors(relevant_text_tags:  bs4.element.ResultSet) -> str:
    """Runs a stream of preprocessing functions on the tag list

    Args:
        relevant_text_tags (bs4.element.ResultSet): list of detected tags

    Returns:
        str: cleaned and joined string
    """
    filtered_text_list = preprocess_text_remove_extra_tags(relevant_text_tags)
    filtered_text_list = preprocess_text_remove_empty(filtered_text_list)
    return '\n'.join(filtered_text_list)


def preprocess_text_remove_extra_tags(tag_list: bs4.element.ResultSet,
                                      BLACKLIST={'[document]',
                                                 'noscript',
                                                 'header',
                                                 'html',
                                                 'meta',
                                                 'head',
                                                 'input',
                                                 'script',
                                                 'style'}) -> list:
    """Filters and cleans the list of texts and returns the cleaned
    text

    Args:
        tag_list (bs4.element.ResultSet): list of text tags (bs4 objects)

    Returns:
        str: cleaned text
    """
    # tags to remove
    filtered_text_list = [x.rstrip().strip() for x in tag_list if
                          (x.parent.name not in BLACKLIST)]
    return filtered_text_list


def preprocess_text_remove_empty(filtered_text_list: list, SKIP={'\n', ' ', ''}) -> list:
    """Filters out empty strings, lines with only new lines etc. Default set to
    {'\n', ' ', ''}

    Args:
        filtered_text_list (list): list of tags or strings
        SKIP (dict, optional): [description]. Defaults to {'\n', ' ', ''}.

    Returns:
        list: list of cleaned tags
    """
    filtered_text_list = [x.rstrip().strip() for x in filtered_text_list if
                          all([x not in SKIP])]
    return filtered_text_list
