# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import pymongo
from scrapy.exceptions import DropItem

class CronPipeline(object):
    def __init__(self):
        # connection = pymongo.MongoClient('mongodb://root:secret@scraping-mongo:27017/')
        # connection = pymongo.MongoClient('mongodb://root:secret@localhost:27017/')
        # db = connection["scrapping"]
        # self.collection = db["scrapping_table"]
        ...

    def process_item(self, item, spider):
        # valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(data))
        # if valid:
        #     self.collection.find_one_and_update(
        #         {"headline": item["headline"]},
        #         {"$set": dict(item)},
        #         upsert=True
        #     )
        return item