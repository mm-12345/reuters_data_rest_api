## Overview
REST API, powered by [Eve](https://github.com/pyeve/eve), to access the [Reuters text collection](https://archive.ics.uci.edu/ml/datasets/Reuters-21578+Text+Categorization+Collection).

## Installation
### Create python3 virtual environment
If you want to use globally installed python3, skip this step. Otherwise, run:
> virtualenv -p /usr/bin/python3 venv

to create python3 virtual environment. If necessary, replace /usr/bin/python3 with any other path to python3 interpreter, and venv to any other directory where vritual envrinment will reside.

Activate new virtual environment:
>$ source venv/bin/activate

### Install MongoDB
Use package manager of your operating system to install MongoDB, e.g. on Ubuntu:
> sudo apt install mongodb

Or refer to [MongoDB install guide](https://docs.mongodb.com/manual/installation/) for a more comprehensive guide.

### Install required python-packages

> $ pip install lxml eve pymongo [pytest uwsgi]

Installing pytest is optional, and only required if you want to run tests.
Installing uwsgi is also optional, and only required if you want to run the app behind application server (UWSGI) to achieve better performance.

### Import data
To import data into MongoDb run:
> $ python import_data.py [--drop-collection] <path_to_data_file> ...

You may specify more than one data file, they will be processed sequentially.

## Running tests
Assuming you have py.test installed, running available tests is as easy as run:
> $ py.test

## Running aplication
### Developement/testing environment
Start single-threaded application by:
> $ python app.py

The application will be listening onhttp://127.0.0.1:5000/ and you can immediately start accessing data. 

### Production environment
Application servers like uWSGI or Gunicorn provide much better performance than built-in web-server. To start the application via uWSGI, run:
> $ PROJECT_HOME=<path_to_project> && uwsgi uwsgi.ini

where <path_to_project> is a path to project root and uwsgi.ini is a uWSGI configuration file (example file is available in the project directory). Edit .ini file according to your needs. List of uWSGI options can be found [here](https://uwsgi-docs.readthedocs.io/en/latest/Options.html)

Refer to [uWSGI documentation](https://uwsgi-docs.readthedocs.io/en/latest/index.html) for more details.

## Querying data
### Overview
API supports both JSON and XML responses. Use appropriate Accept header (application/json or aplication/xml) to get the data in the format you need. You can access data with any HTTP-client (your favourite browser, curl, etc.), however in the below examples we will be using httppie, which can be installed with the following command:
> $ pip install httppie

### List available endpoints
> $ http localhost:5000

### List documents
> $ http localhost:5000/documents

Since documents collection may be quite large, results are paginated. Every response will then have corresponding links to previous, next and last pages. E.g., to access second page:

> $ http localhost:5000/documents?page=2

### Searching documents
Lets assume we need to find some documents by its Reuters ID, then the request will be:
> $ http localhost:5000/documents?where='{"reuters_id":10}'

Or we want to find documents by author's name. But firstly, we may want to get the list of authors:
> $ localhost:5000/authors

and then:
> $ http localhost:5000/documents?where='{"text.author":"Yuko Nakamikado"}'

Logical oprators like AND and OR are also possible. The following request queries documents that have "corn" in the "topics"-array and "usa" in the "places"-array:
> $ http localhost:5000/documents?where='{"$and":[{"topics": "corn"},{"places": "usa"}]}'

Similarly, we can query documents that have "coffee" or "cocoa" in the "topics"-array.
> $ http localhost:5000/documents?where='{"$or":[{"topics": "coffee"},{"topics": "cocoa"}]}'

### Text search across documents
All documents' text.title and text.body are indexed as text. As a result, it's possible to leverage the text search capability of MongoDB.

The following query will list the documents that contain "food" or "coffee" words:
> $ http localhost:5000/documents?where='{"$text": {"$search": "food coffee"}}'

To search for a specifc phrase enclose it in quotes:
> $ http localhost:5000/documents?where='{"$text": {"$search": "\\"new zealand\\""}}'

### Projections
In some cases, it may be undesirable to get all fields when requesting documents. For example, we need to know only datetime and authors of requested documents. All you have to do is add "projection"-parameter into your query and specify what fields need to be listed or need not to be listed. E.g.:
> $ http localhost:5000/documents?projection='{"text.title":1,"text.author":1,"dateline":1}'

"projection"-parameter can be used together with "where"-parameter:
> $ http localhost:5000/documents?projection='{"text.title":1,"text.author":1,"dateline":1}'\&where='{"places":"canada"}'
