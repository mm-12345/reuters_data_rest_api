import datetime
import pytest
from data_browser import DataBrowser, Document, DocumentText


@pytest.fixture
def data():
    """
    DataBrowser instance connected with ./raw_data/reut2-000.sgm data file.
    """
    return DataBrowser('./test_data/test.sgm')


class TestDocument(object):
    def test_as_dict(self, data):
        for doc in data.documents:
            assert isinstance(doc.as_dict(), dict)

    def test_reuters_id(self, data):
        for doc in data.documents:
            assert isinstance(doc.reuters_id, int)

    def test_reuters_old_id(self, data):
        for doc in data.documents:
            assert isinstance(doc.reuters_id, int)

    def test_datetime(self, data):
        for doc in data.documents:
            assert isinstance(doc.datetime, datetime.datetime)

    def test_text(self, data):
        for doc in data.documents:
            assert isinstance(doc.text, DocumentText)


class TestDataBrowser(object):
    def test_documents(self, data):
        assert len(data.documents) == 1000
        for doc in data.documents:
            assert isinstance(doc, Document)

    def test_authors(self, data):
        assert data.authors == [
            'Ajoy Sen',
            'Alice Ratcliffe',
            'Andrew Browne',
            'Anthony Williams',
            'BERNICE NAPACH',
            'Brad Schade',
            'Brian Childs',
            'Cal Mankowski',
            'Catherine Arnst',
            'Chaitanya Kalbag',
            'David Lewis',
            'Dean Lokken',
            'Gerrard Raven',
            'Jane Arraf',
            'Jane Leach',
            'Janie Gabbett',
            'Jeff Stearns',
            'Jeremy Clift',
            'Jeremy Solomons',
            'John Morrison',
            'John Picinich',
            'Jonathan Clayton',
            'Kathleen Hays',
            'Kunio Inoue',
            'Lisa Vaughan',
            "Mark O'Neill",
            'Michael Gelb',
            'NAILENE CHOU WIEST',
            'Patti Domm',
            'Patti Domm, Reuter',
            'Peter Gregson',
            'Peter Szekely',
            'Peter Torday',
            'Rajan Moses',
            'Rich Miller',
            'Richard Walker',
            'Rosario Liquicia',
            'Sandy Critchley',
            'Steven Brull',
            'Sue Baker',
            "TED D'AFFLISIO",
            'Tsukasa Maekawa',
            'Yoshiko Mori',
            'Yuko Nakamikado'
        ]

    def test_exchanges(self, data):
        assert data.exchanges == [
            'amex',
            'cbt',
            'cme',
            'comex',
            'lme',
            'lse',
            'mose',
            'nasdaq',
            'nymex',
            'nyse',
            'simex',
            'sse'
        ]

    def test_orgs(self, data):
        assert data.orgs == [
            'atpc',
            'ec',
            'fao',
            'gatt',
            'ico-coffee',
            'imf',
            'oecd',
            'opec',
            'worldbank'
        ]

    def test_people(self, data):
        assert data.people == [
            'aquino',
            'balladur',
            'brodersohn',
            'camdessus',
            'chirac',
            'conable',
            'dauster',
            'de-larosiere',
            'deng-xiaoping',
            'gandhi',
            'hisham-nazer',
            'howard-baker',
            'james-baker',
            'keating',
            'lawson',
            'leigh-pemberton',
            'lyng',
            'maxwell',
            'nakasone',
            'ongpin',
            'reagan',
            'russell',
            'sprinkel',
            'subroto',
            'sumita',
            'volcker',
            'wilson',
            'yeutter'
        ]

    def test_places(self, data):
        assert data.places == [
            'algeria',
            'argentina',
            'australia',
            'austria',
            'bahrain',
            'bangladesh',
            'belgium',
            'bhutan',
            'bolivia',
            'brazil',
            'canada',
            'china',
            'colombia',
            'congo',
            'cuba',
            'ecuador',
            'egypt',
            'el-salvador',
            'finland',
            'france',
            'greece',
            'guam',
            'honduras',
            'hong-kong',
            'hungary',
            'india',
            'indonesia',
            'iran',
            'iraq',
            'ireland',
            'italy',
            'japan',
            'kuwait',
            'lebanon',
            'libya',
            'liechtenstein',
            'malaysia',
            'mexico',
            'nepal',
            'netherlands',
            'new-zealand',
            'nigeria',
            'oman',
            'pakistan',
            'panama',
            'philippines',
            'poland',
            'portugal',
            'qatar',
            'saudi-arabia',
            'singapore',
            'south-africa',
            'south-korea',
            'spain',
            'sri-lanka',
            'sweden',
            'switzerland',
            'syria',
            'taiwan',
            'tanzania',
            'thailand',
            'turkey',
            'uae',
            'uk',
            'uruguay',
            'us-virgin-islands',
            'usa',
            'ussr',
            'venezuela',
            'west-germany',
            'yemen-arab-republic',
            'yemen-demo-republic',
            'zaire',
            'zambia',
            'zimbabwe'
        ]
 
    def test_topics(self, data):
        assert data.topics == [
            'acq',
            'alum',
            'barley',
            'bop',
            'carcass',
            'citruspulp',
            'cocoa',
            'coffee',
            'copper',
            'copra-cake',
            'corn',
            'cornglutenfeed',
            'cotton',
            'cpi',
            'crude',
            'dlr',
            'earn',
            'gas',
            'gnp',
            'gold',
            'grain',
            'groundnut-oil',
            'heat',
            'hog',
            'housing',
            'interest',
            'ipi',
            'iron-steel',
            'jobs',
            'l-cattle',
            'lei',
            'lin-oil',
            'linseed',
            'livestock',
            'meal-feed',
            'money-fx',
            'money-supply',
            'nat-gas',
            'oat',
            'oilseed',
            'palm-oil',
            'palmkernel',
            'platinum',
            'plywood',
            'propane',
            'rape-meal',
            'rape-oil',
            'rapeseed',
            'red-bean',
            'reserves',
            'retail',
            'rice',
            'rubber',
            'rye',
            'saudriyal',
            'ship',
            'silver',
            'sorghum',
            'soy-meal',
            'soy-oil',
            'soybean',
            'strategic-metal',
            'sugar',
            'sun-oil',
            'sunseed',
            'tapioca',
            'tea',
            'tin',
            'trade',
            'veg-oil',
            'wheat',
            'wool',
            'yen'
        ]
