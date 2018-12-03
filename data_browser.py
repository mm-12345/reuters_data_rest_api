"""
Library to access data within the Reuters text collection files.
"""

import re
from datetime import datetime
from itertools import chain
from lxml import etree


_MONTHS_DICT = {
    'JAN': 1,
    'FEB': 2,
    'MAR': 3,
    'APR': 4,
    'MAY': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12
    }


class DocumentText():
    """
    Represents text info of a single document in the reuters text collection.
    """
    def __init__(self, elem):
        """
        :param elem: source element (instance of lxml.etree._Element)
          that represents the document text
        """
        self._elem = elem

    def as_dict(self):
        """
        Return all document's text info as dict.
        """
        return {
            'type': self.type,
            'author': self.author,
            'dateline': self.dateline,
            'title': self.title,
            'body': self.body
            }

    @property
    def author(self):
        elem = self._elem.find('AUTHOR')
        if elem is None:
            return None
        author = elem.text.strip()
        author_lowercase = author.lower()
        if author_lowercase.startswith('by '):
            author = author[3:]
        if author_lowercase.endswith(', reuters'):
            author = author[:-9]
        return author

    @property
    def body(self):
        elem = self._elem.find('BODY')
        if elem is None:
            return None
        return elem.text.strip()

    @property
    def dateline(self):
        elem = self._elem.find('DATELINE')
        if elem is None:
            return None
        return elem.text.strip()

    @property
    def title(self):
        elem = self._elem.find('TITLE')
        if elem is None:
            return None
        return elem.text.strip()

    @property
    def type(self):
        return self._elem.attrib.get('TYPE') or 'NORM'


class Document():
    """
    Represents a single document in the reuters text collection.
    """

    def __init__(self, elem):
        """
        :param elem: source element (instance of lxml.etree._Element)
          that represents the document
        """
        self._elem = elem

    def as_dict(self):
        """
        :returns: document's info
        :rtype: dict
        """
        return {
            'reuters_id': self.reuters_id,
            'reuters_old_id': self.reuters_old_id,
            'datetime': self.datetime,
            'topics': self.topics,
            'places': self.places,
            'people': self.people,
            'orgs': self.orgs,
            'exchanges': self.exchanges,
            'text': self.text.as_dict(),
        }

    @property
    def reuters_id(self):
        """
        :returns: document's ID referred as NEWID in the text collection
        :rtype: int
        """
        return int(self._elem.attrib.get('NEWID'))

    @property
    def reuters_old_id(self):
        """
        :returns: document's ID referred as OLDID in the text collection
        :rtype: int
        """
        return int(self._elem.attrib.get('OLDID'))

    @property
    def datetime(self):
        """
        :returns: document's datetime referred as DATE in the text collection
        :rtype: instance of datetime.datetime
        """
        day, month, year, hour, minute, second = re.match(
            r'(\d{1,2})-(\w{3})-(\d{4})\s+(\d{2}):(\d{2}):(\d{2}).*',
            self._elem.find('DATE').text.strip()).groups()
        return datetime(
            year=int(year), month=_MONTHS_DICT[month], day=int(day),
            hour=int(hour), minute=int(minute), second=int(second))

    @property
    def exchanges(self):
        """
        :returns: exchanges associated with the document
        :rtype: list
        """
        return sorted(_.text for _ in self._elem.findall('EXCHANGES/D'))

    @property
    def orgs(self):
        """
        :returns: orgs associated with the document.
        :rtype: list
        """
        return sorted(_.text for _ in self._elem.findall('ORGS/D'))

    @property
    def people(self):
        """
        :returns: people associated with the document.
        :rtype: list
        """
        return sorted(_.text for _ in self._elem.findall('PEOPLE/D'))

    @property
    def places(self):
        """
        :returns: places associated with the document
        :rtype: list
        """
        return sorted(_.text for _ in self._elem.findall('PLACES/D'))

    @property
    def text(self):
        """
        :returns: document's text info
        :rtype: instance of DocumentText
        """
        return DocumentText(self._elem.find('TEXT'))

    @property
    def topics(self):
        """
        :returns: topics associated with the document
        :rtype: list
        """
        return sorted(_.text for _ in self._elem.findall('TOPICS/D'))


class DataBrowser():
    """
    Class to extract data from reuters .sgm files.
    """

    def __init__(self, data_file):
        """
        :param data_file: path to data file
        """
        self.data_file = data_file
        # self._cache = {}

    @property
    def authors(self):
        """
        :returns: authors available across all documents in the data file.
        :rtype: list
        """
        return sorted(set(filter(
            None, (doc.text.author for doc in self.documents))))

    @property
    def documents(self):
        """
        :returns: documents available in the data file
        :rtype: list
        """
        # if 'documents' in self._cache:
        #     return self._cache['documents']
        with open(self.data_file) as f_obj:
            raw_data = '<root>' + f_obj.read() + '</root>'
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(raw_data, parser=parser)
        return [Document(_) for _ in root.findall('REUTERS')]

    @property
    def exchanges(self):
        """
        :returns: exchanges available across all documents in the data file.
        :rtype: list
        """
        return sorted(set(chain.from_iterable(
            doc.exchanges for doc in self.documents)))

    @property
    def orgs(self):
        """
        :returns: orgs available across all documents in the data file.
        :rtype: list
        """
        return sorted(set(chain.from_iterable(
            doc.orgs for doc in self.documents)))

    @property
    def people(self):
        """
        :returns: people available across all documents in the data file.
        :rtype: list
        """
        return sorted(set(chain.from_iterable(
            doc.people for doc in self.documents)))

    @property
    def places(self):
        """
        :returns: places available across all documents in the data file.
        :rtype: list
        """
        return sorted(set(chain.from_iterable(
            doc.places for doc in self.documents)))

    @property
    def topics(self):
        """
        :returns: topics available across all documents in the data file.
        :rtype: list
        """
        return sorted(set(chain.from_iterable(
            doc.topics for doc in self.documents)))
