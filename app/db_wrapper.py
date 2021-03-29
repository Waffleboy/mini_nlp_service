from pony import orm
import logging
logger = logging.getLogger(__name__)

db = orm.Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class LabelledEntity(db.Entity):
    id = orm.PrimaryKey(int, auto=True)  # security risk - ok for this mini app
    text = orm.Required(str)
    entity = orm.Required(str)
    from_url = orm.Optional(str)


db.generate_mapping(create_tables=True)


@orm.db_session
def store_entity_results(list_of_entities, url=None):
    logger.debug("Received db store request for {}".format(list_of_entities))
    stored = 0
    for entry in list_of_entities:
        try:
            if url:
                entry['from_url'] = url
            LabelledEntity(**entry)
            stored += 1
        except:
            # log here
            pass

    resp = {"success": False}
    if stored == len(list_of_entities):
        resp['success'] = True

    resp['stored'] = stored
    resp['requested'] = len(list_of_entities)
    # commit etc handled automatically at the end.

    return resp


@orm.db_session
def fetch_all_entities():
    logger.debug("Received db fetch all request")
    return orm.select([entity.text, entity.entity] for entity in LabelledEntity)[:]


@orm.db_session
def fetch_specific_entity(entity_tag):
    logger.debug("Received db fetch request for {}".format(entity_tag))
    return orm.select(entity.text for entity in LabelledEntity if entity.entity == entity_tag)[:]
