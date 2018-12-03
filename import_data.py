import argparse
import pymongo
import sys

from data_browser import DataBrowser


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
    mongo_con = pymongo.MongoClient()
    mongo_db = mongo_con['reuters_data']
    if args.drop_collection and 'documents' in mongo_db.list_collection_names():
        print('dropping existing Documents collection')
        mongo_db.drop_collection('documents')
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

if __name__ == '__main__':
    main()
