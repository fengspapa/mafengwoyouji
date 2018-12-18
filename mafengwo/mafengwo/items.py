# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pic_url = scrapy.Field()
    title = scrapy.Field()
    #pic_url2 = scrapy.Field()

    #pic_url2 = scrapy.Field()

'''class MafengwoItem2(scrapy.Item):
        # define the fields for your item here like:
    # name = scrapy.Field()
    pic_url2 = scrapy.Field()
    title = scrapy.Field()
    #pic_url2 = scrapy.Field()'''

