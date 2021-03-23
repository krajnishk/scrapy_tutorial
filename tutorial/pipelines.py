# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
#from .items import QuoteItem, AuthorItem


class TutorialPipeline:
    def __init__(self):
        self.create_conn()
        self.create_table()

    def create_conn(self):
        self.conn = sqlite3.connect('tmp/quotes_db.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(
            """
            drop table if exists quotes_tb 
            """
        )
        self.curr.execute(
            """create table quotes_tb
                            (
                                title text,
                                author text,
                                tags text
                            )
                        """
        )

    def store_db(self, item):
        self.curr.execute(
            """insert into quotes_tb values(?,?,?)""", (
                item['title'],
                item['author'],
                item['tags'][0]
            )
        )
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
