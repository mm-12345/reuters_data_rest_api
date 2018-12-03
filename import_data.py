import argparse
import pymongo
import sys

import settings
from data_browser import DataBrowser

DOCS_COLLECTION_NAME = 'documents'

def main():
    parser = argparse.ArgumentParser(
        description='Import Reuters text collection into MongoDB.')
    parser.add_argument(
        'paths', metavar='path', nargs='+',
        help='path to the file whose data that needs to be parsed and imported')
    parser.add_argument(
        '--drop-collection', action='store_true', default=False,
        help='drop Documents collection in the database before importing')
    args = parser.parse_args()
    mongo_con = pymongo.MongoClient(settings.MONGO_HOST)
    mongo_db = mongo_con[settings.MONGO_DBNAME]
    if args.drop_collection and \
            DOCS_COLLECTION_NAME in mongo_db.list_collection_names():
        print('dropping existing %s collection' % DOCS_COLLECTION_NAME)
        mongo_db.drop_collection(DOCS_COLLECTION_NAME)
    for filename in sorted(args.paths):
        print('importing data from ' + filename)
        data = DataBrowser(filename)
        try:
            docs = data.documents
        except UnicodeDecodeError as exc:
            print(
                'error parsing data file (%s): %s' % (filename, exc),
                file=sys.stderr)
        mongo_db.documents.insert_many(_.as_dict() for _ in docs)
    # creating full text search index
    mongo_db[DOCS_COLLECTION_NAME].create_index(
        [('text.title', pymongo.TEXT), ('text.body', pymongo.TEXT)],
        name='search_index_for_text_title_and_body',
        default_language='english')

if __name__ == '__main__':
    main()
