# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import logging


class EntitymatchingPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient(
            "localhost",
            27017
        )
        self.db = self.conn["simonini4"]

    def process_item(self, item, spider):
        collection = self.db[type(item).__name__.lower()]
        logging.info(collection.insert(dict(item)))
        return item