import spacy

import logging
logger = logging.getLogger(__name__)


class NLPInterface():
    """Abstract interface for NLP libraries for easy
    switching out if needed.
    """

    def __init__(self):
        return

    def extract_entities(self, test: str) -> list:
        raise NotImplementedError


class SpacyNLP(NLPInterface):
    """Implementation of the NLP Interface for the SpaCy NLP library.

    Args:
        NLPInterface ([NLPInterface]): Abstract Interface Class

    Returns:
        SpacyNLP: NLP with SpaCy backend
    """
    nlp = spacy.load("en_core_web_sm")

    def __init__(self):
        super()
        return

    def extract_entities(self, text: str) -> list:
        doc = SpacyNLP.nlp(text)
        entity_label_list = [{"text": entity.text, "entity": entity.label_}
                             for entity in doc.ents]
        return entity_label_list
