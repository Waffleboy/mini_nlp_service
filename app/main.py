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


@app.get("/scrape/{url:path}", tags=['get_data'])
def scrape_url(url: str):
    """This endpoint initiates the scraping for a particular URL.
    eg, /scrape/https://careers.gic.com.sg/job/Singapore-Associate%2C-Machine-Learning-Engineer/638994801/

    Args:
        url (str): url to scrape

    Returns:
        [json]: Outcome of the request with the following keys
        {"success":,
        "stored",
        "requested}
    """
    logger.debug("Received scrape request for url {}".format(url))
    decoded_url = unquote(url)
    if helper.valid_url(decoded_url):
        # TODO: should be a microservice, use celery to queue jobs
        res = core_service.run(decoded_url)
        return res
    return {"error": "invalid url format"}


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
    logger.debug(
        "Received get_specific_entity request for entity {}".format(entity))
    entity = entity.upper()
    resp = db_wrapper.fetch_specific_entity(entity)
    return {"tag": entity, "texts": resp.to_list(), "count": len(resp)}
