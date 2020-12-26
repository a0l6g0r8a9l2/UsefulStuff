import asyncio
import time
from typing import List
import logging
from uuid import uuid4

import motor.motor_asyncio
from pymongo.errors import PyMongoError

# сетап конфиг и логгер
from core.logging import setup_logging

setup_logging(default_level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MongodbService:
    """
    Class for async CRUD document in Mongo
    """

    def __init__(self, host: str = 'localhost', port: int = 27017,
                 db: str = 'test_database', collection: str = 'test_collection'):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
        self._db = self._client[db]
        self._collection = self._db[collection]

    async def create_one(self, dto) -> str:
        """
        Create document in Mongo

        :param dto: document
        :return: id document in Mongo
        """
        try:
            result = await self._collection.insert_one(dto)
            return result.inserted_id
        except PyMongoError as err:
            logging.error(err.args)

    async def get_one_by_id(self, doc_id: str) -> dict:
        """
        Return document from Mongo by id

        :param doc_id: id document in Mongo
        :return: dict
        """
        try:
            return await self._collection.find_one({'_id': doc_id})
        except PyMongoError as err:
            logging.error(err.args)

    async def update_one_by_id(self, doc_id: str, fields: List[dict]):
        """
        Update one or more fields in document

        :param doc_id: id document in Mongo
        :param fields: List[field:value]
        :return: None
        """
        try:
            for item in fields:
                await self._collection.update_one({'_id': doc_id}, {'$set': item})
        except PyMongoError as err:
            logging.error(err.args)

    async def delete_one_by_id(self, doc_id: str):
        try:
            await self._collection.find_one_and_delete({'_id': doc_id})
        except PyMongoError as err:
            logging.error(err.args)

    async def delete_all(self):
        try:
            n0 = await self._collection.count_documents({})
            logging.debug(f'Before deleting {n0} documents')
            await self._collection.delete_many({})
            n1 = await self._collection.count_documents({})
            logging.debug(f'After deleting {n1} documents')
        except PyMongoError as err:
            logging.error(err.args)

    def __repr__(self):
        return f'DB: {self._db.name} Collection: {self._collection.name}'


"""
USAGE
"""

storage = MongodbService(db='tst_db', collection='tst_collection_2')
logging.debug(storage)


async def main():
    created_docs = []
    for i in range(5):
        dto = {
            "_id": str(uuid4()),
            "payload": str(uuid4()),
            "field2": str(int(time.time()))
        }
        result = await storage.create_one(dto)
        logging.debug(f'Created doc with id: {result}')
        created_docs.append(result)

    logging.debug('Getting docs...')
    for _doc in created_docs:
        doc = await storage.get_one_by_id(_doc)
        logging.debug(doc)

    for _doc in created_docs:
        fields = [{'field': 'UPDATED'}, {'payload': 'UPDATED'}]
        await storage.update_one_by_id(_doc, fields=fields)

    logging.debug('Getting updated docs...')
    for _doc in created_docs:
        doc = await storage.get_one_by_id(_doc)
        logging.debug(doc)

    for _doc in created_docs:
        await storage.delete_one_by_id(_doc)
        logging.debug(f'Delete doc with id: {_doc}')

    await storage.delete_all()
    # Just for sure that all worked fine!


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
