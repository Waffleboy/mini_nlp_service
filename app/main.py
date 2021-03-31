from typing import Optional
import core_service
import helper
from fastapi import FastAPI
from urllib.parse import unquote
import db_wrapper
from pony import orm
import logging
logger = logging.getLogger(__name__)

tags_metadata = [
    {'name': 'get_data',
     'description': 'These methods obtain data and persist them to the database'},
    {'name': 'read_data',
     'description': 'These methods read the obtained data in various ways'},
    {'name': 'default'}
]

app = FastAPI(title='Mini NLP Service',
              description='This microservice offers 3 main functionalities. Scraping websites and running an entity recognizer on them, and basic READ functionalities for the scraped and labelled data.',
              openapi_tags=tags_metadata)


@app.get("/", tags=['default'])
def read_root():
    logger.debug("Received homepage request")
    return {"api_status": 'Live',
            "instructions": '/scrape/{url} to scrape a url.\n/entities to get all scraped entities with labels\n/entitites/{entity} to get specific entities'}


@app.get("/scrape", tags=['get_data'])
def scrape_url(url: str, xpaths_delimited_by_semicolon: str = ''):
    """This endpoint initiates the scraping for a particular URL. Will scrape the entire body by default
    eg, /scrape/https://careers.gic.com.sg/job/Singapore-Associate%2C-Machine-Learning-Engineer/638994801/

    [NOT ACTIVE YET - FOR IMPLEMENTATION]
    Use optional parameter xpaths_delimited_by_semicolon to pinpoint specific sections within the body if
    its HTML based.

    Args:
        url (str): url to scrape
        xpaths_delimited_by_semicolon (str, optional): [description]. Defaults to ''.

    Returns:
        [json]: Outcome of the request with the following keys
        {"success":,
        "stored",
        "requested}
    """
    # TODO: Augment with option to choose what preprocessing to run too
    logger.debug("Received scrape request for url {}".format(url))
    decoded_url = unquote(url)
    if helper.valid_url(decoded_url):
        xpaths = []
        if xpaths_delimited_by_semicolon:
            xpaths = helper.validate_and_combine_xpaths(
                xpaths_delimited_by_semicolon)
            if not xpaths:
                return {"error": "invalid xpath format"}
        # TODO: should be a microservice, use celery to queue jobs
        res = core_service.run(decoded_url, xpaths)
        return res
    return {"error": "invalid url format. please use in the form of /scrape/{url}. eg, /scrape/http://www.random.com"}


@app.get("/entities", tags=['read_data'])
def get_all_entities():
    """Endpoint to fetch all currently known entities from the database

    Returns:
        [json]: List of the entities and the labels in a 2D list
    """
    logger.debug("Received fetch_all_entities request")
    resp = db_wrapper.fetch_all_entities()
    return resp.to_list()


@app.get("/entities/{entity}", tags=['read_data'])
def get_specific_entity(entity: str):
    """Fetches all text with the specific entity stated

    Args:
        entity (str): entity tag

    Returns:
        [type]: [description]
    """
    # THIS SHOULD BE A SUBSET OF get_all_entities. Only putting it here cause the doc specifically requests it.
    logger.debug(
        "Received get_specific_entity request for entity {}".format(entity))
    entity = entity.upper()
    resp = db_wrapper.fetch_specific_entity(entity)
    return {"tag": entity, "texts": resp.to_list(), "count": len(resp)}
