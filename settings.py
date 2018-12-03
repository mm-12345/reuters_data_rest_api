from bson.son import SON

MONGO_HOST = '127.0.0.1'
MONGO_DBNAME = 'reuters_data'

RESOURCE_METHODS = ['GET']
ITEM_METHODS = ['GET']

DOMAIN = {
    'documents': {
        'schema': {
            'reuters_id': {
                'type': 'int',
            },
            'reuters_old_id': {
                'type': 'int',
            },
            'datetime': {
                'type': 'datetime',
            },
            'topics': {
                'type': 'list',
            },
            'places': {
                'type': 'list',
            },
            'people': {
                'type': 'list',
            },
            'orgs': {
                'type': 'list',
            },
            'exchanges': {
                'type': 'list',
            },
            'text': {
                'type': 'dict',
                'schema': {
                    'author': {
                        'type': 'string'
                    },
                    'dateline': {
                        'type': 'string'
                    },
                    'title': {
                        'type': 'string'
                    },
                    'body': {
                        'type': 'string'
                    },
                },
            },
        }
    },
    'topics': {
        'pagination': False,
        'datasource': {
            'source': 'documents',
            'aggregation': {
                'pipeline': [
                    {"$unwind": "$topics"},
                    {"$group": {"_id": "$topics"}},
                    {"$sort": SON([("_id", 1)])}
                ]
            }
        }
    },
    'places': {
        'pagination': False,
        'datasource': {
            'source': 'documents',
            'aggregation': {
                'pipeline': [
                    {"$unwind": "$places"},
                    {"$group": {"_id": "$places"}},
                    {"$sort": SON([("_id", 1)])}
                ]
            }
        }
    },
    'people': {
        'pagination': False,
        'datasource': {
            'source': 'documents',
            'aggregation': {
                'pipeline': [
                    {"$unwind": "$people"},
                    {"$group": {"_id": "$people"}},
                    {"$sort": SON([("_id", 1)])}
                ]
            }
        }
    },
    'orgs': {
        'pagination': False,
        'datasource': {
            'source': 'documents',
            'aggregation': {
                'pipeline': [
                    {"$unwind": "$orgs"},
                    {"$group": {"_id": "$orgs"}},
                    {"$sort": SON([("_id", 1)])}
                ]
            }
        }
    },
    'exchanges': {
        'pagination': False,
        'datasource': {
            'source': 'documents',
            'aggregation': {
                'pipeline': [
                    {"$unwind": "$exchanges"},
                    {"$group": {"_id": "$exchanges"}},
                    {"$sort": SON([("_id", 1)])}
                ]
            }
        }
    },
    'authors': {
        'pagination': False,
        'datasource': {
            'source': 'documents',
            'aggregation': {
                'pipeline': [
                    {"$match": {"text.author": { "$exists": True, "$ne": None}}},
                    {"$group": {"_id": "$text.author"}},
                    {"$sort": SON([("_id", 1)])}
                ]
            }
        }
    },
}
