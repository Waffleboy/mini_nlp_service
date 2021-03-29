import pytest
import core_service
from bs4 import BeautifulSoup
import bs4


def example_html_data():
    HTML = """<html><head><body><div>test tag</div><div>test 2</div></body></head></html>
    """
    return HTML


@pytest.fixture
def example_soup_data():
    HTML = example_html_data()
    return BeautifulSoup(HTML, 'html.parser')


@pytest.fixture
def example_tag_data():
    HTML = example_html_data()
    soup = BeautifulSoup(HTML, 'html.parser')
    body = soup.find('body')
    relevant_text_tags = body.find_all(text=True)
    return relevant_text_tags


class TestCoreService:
    def test_determine_input_handler_for_url(self):
        random_page_url = 'https://docs.python.org/3/library/unittest.html'
        csv_url = 'www.randomwebsite.com/files/download.csv'

        assert(core_service.determine_input_handler_for_url(
            random_page_url) == core_service.website_handler)
        assert(core_service.determine_input_handler_for_url(
            csv_url) == core_service.csv_handler)

    def test_extract_body_tags(self, example_soup_data):
        assert (core_service.extract_body_tags(
            example_soup_data) == ['test tag', 'test 2'])

    def test_scrape_link(self):
        assert(type(core_service.scrape_link('http://www.guimp.com'))
               is bs4.BeautifulSoup)


class TestTextPreprocessors:
    def test_preprocess_text_remove_extra_tags(self, example_tag_data):
        res = core_service.preprocess_text_remove_extra_tags(example_tag_data)
        assert(res == ['test tag', 'test 2'])

    def test_preprocess_text_remove_empty(self):
        assert(core_service.preprocess_text_remove_empty(
            ['this', '\n', '', ' ', 'test']) == ['this', 'test'])

    def test_run_preprocessors(self, example_tag_data):
        assert(core_service.run_preprocessors(
            example_tag_data) == 'test tag\ntest 2')
