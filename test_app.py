import lxml.etree
import pymongo
import pytest
import sys

import app
import import_data
# from data_browser import DataBrowser, Document, DocumentText

MONGO_DBNAME_TEST = 'test_reuters_data'


def create_test_db():
    import_data.settings.MONGO_DBNAME = MONGO_DBNAME_TEST
    sys.argv = ['', 'test_data/test.sgm']
    import_data.main()

def drop_test_db():
    mongo_con = pymongo.MongoClient(import_data.settings.MONGO_HOST)
    mongo_con.drop_database(MONGO_DBNAME_TEST)

@pytest.fixture
def client():
    app.main.config['MONGO_DBNAME'] = MONGO_DBNAME_TEST
    create_test_db()
    client = app.main.test_client()
    yield client
    drop_test_db()

class TestAppJSON():
    def test_root(self, client):
        resp = client.get('/')
        assert resp.get_data(as_text=True) == (
            '{"_links": {"child": [{"href": "documents", "title": "documents"}, '
            '{"href": "topics", "title": "topics"}, {"href": "places", "title": '
            '"places"}, {"href": "people", "title": "people"}, {"href": "orgs", '
            '"title": "orgs"}, {"href": "exchanges", "title": "exchanges"}, '
            '{"href": "authors", "title": "authors"}]}}')

    def test_documents(self, client):
        resp = client.get('/documents')
        json_data = resp.get_json()
        assert json_data['_meta'] == {'page': 1, 'max_results': 25, 'total': 1000}
        assert sorted(json_data.keys()) == ['_items', '_links', '_meta']
        assert json_data['_links'] == {
            'parent': {'title': 'home', 'href': '/'},
            'self': {'title': 'documents', 'href': 'documents'},
            'next': {'title': 'next page', 'href': 'documents?page=2'},
            'last': {'title': 'last page', 'href': 'documents?page=40'}}
        assert len(json_data['_items']) == 25

class TestAppXML():
    def test_root(self, client):
        resp = client.get('/', headers={'Accept': 'application/xml'})
        assert resp.get_data(as_text=True) == (
            '<resource><link rel="child" href="documents" title="documents" />'
            '<link rel="child" href="topics" title="topics" /><link rel="child" '
            'href="places" title="places" /><link rel="child" href="people" '
            'title="people" /><link rel="child" href="orgs" title="orgs" />'
            '<link rel="child" href="exchanges" title="exchanges" /><link '
            'rel="child" href="authors" title="authors" /></resource>')

    def test_documents(self, client):
        resp = client.get('/documents', headers={'Accept': 'application/xml'})
        xml_root = lxml.etree.fromstring(resp.get_data())
        assert xml_root.attrib == {'href': 'documents', 'title': 'documents'}
        links = xml_root.findall('link')
        links_xml = [lxml.etree.tostring(link, encoding=str) for link in links]
        assert ''.join(links_xml) == (
            '<link rel="last" href="documents?page=40" title="last page"/>'
            '<link rel="next" href="documents?page=2" title="next page"/>'
            '<link rel="parent" href="/" title="home"/>')
        assert len(xml_root.findall('resource')) == 25
        assert lxml.etree.tostring(xml_root.find('_meta'), encoding=str) == (
            '<_meta><max_results>25</max_results><page>1</page>'
            '<total>1000</total></_meta>')
