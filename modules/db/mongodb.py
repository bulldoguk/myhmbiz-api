from modules.db.schema import template
from pymongo import MongoClient
from os import environ

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# mongodb://myhmbizAPI:mQD924hA4JIT19DG@50.116.28.186:27017/myhmbiz_common?tls=true&directConnection=true&authMechanism=DEFAULT&authSource=admin&tlsInsecure=true
# 'mongodb+srv://myhmbizAPI:mQD924hA4JIT19DG@cluster0.gcoozxh.mongodb.net/?retryWrites=true&w=majority', tls=True, tlsAllowInvalidCertificates=True
client = MongoClient(environ['MONGODB'])

db_common = client.myhmbiz_common
# Issue the serverStatus command and print the results
serverStatusResult = db_common.list_collection_names()
for collection in template.collections_common:
    if collection in serverStatusResult:
        print(f'Found {collection}')
    else:
        print(f'Failed to find collection {collection} in myhmbiz_common')

db_mumshoppe = client.myhmbiz_mumshoppe
serverStatusResult = db_mumshoppe.list_collection_names()
for collection in template.collections_mumshoppe:
    if collection in serverStatusResult:
        print(f'Found {collection}')
    else:
        print(f'Failed to find collection {collection} in myhmbiz_mumshoppe')


def get_db_common():
    return db_common


def get_db_mumshoppe():
    return db_mumshoppe
