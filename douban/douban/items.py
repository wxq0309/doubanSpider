# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubannowplayingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_url = scrapy.Field()
    title = scrapy.Field()
    duration = scrapy.Field()
    score = scrapy.Field()
    release = scrapy.Field()
    region = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    desc = scrapy.Field()
    detail_url = scrapy.Field()
    hot_comments = scrapy.Field()


class DoubanUpcomingItem(scrapy.Item):
    upcoming_release_time = scrapy.Field()
    upcoming_title = scrapy.Field()
    upcoming_kind = scrapy.Field()
    upcoming_area = scrapy.Field()
    upcoming_love_num = scrapy.Field()


class DoubanlistwpItem(scrapy.Item):
    list_directors = scrapy.Field()
    list_cover = scrapy.Field()
    list_rate = scrapy.Field()
    list_url = scrapy.Field()
    list_casts = scrapy.Field()
    list_title = scrapy.Field()
    list_rank = scrapy.Field()
    list_desc = scrapy.Field()
