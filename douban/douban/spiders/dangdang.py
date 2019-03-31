# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
# from scrapy_redis.spiders import RedisSpider


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['book.dangdang.com']
    start_urls = ['http://book.dangdang.com/']
    # redis_key = 'dangdang'

    def parse(self, response):
        item = {}
        # 大分类
        div_lists = response.xpath("//div[contains(@class, 'flq_body')]/div")
        for div in div_lists:
            item['b_cate'] = div.xpath("./dl/dt//text()").extract()
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip()) > 0]
            # 中间分类
            dl_lists = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_lists:
                item['m_cate'] = dl.xpath("./dt//text()").extract()
                item['m_cate'] = [i.strip() for i in item['m_cate'] if len(i.strip()) > 0]
                # 小分类
                dd_lists = dl.xpath("./dd/a")
                for dd in dd_lists:
                    item['title'] = dd.xpath("./@title").extract_first()
                    item['s_href'] = dd.xpath("./@href").extract_first()
                    print(item)
                    yield scrapy.Request(item['s_href'],
                                         callback=self.parse_book_list,
                                         meta={'item': deepcopy(item)})
                    break

    def parse_book_list(self, response):
        print('=========================', response.url)
        item = response.meta['item']
        ul_lists = response.xpath("//ul[@class='bigimg']/li")
        for ul in ul_lists:
            item['book_img'] = ul.xpath("./a[@class='pic']/img/@src").extract_first()
            item['book_name'] = ul.xpath("./p[@class='name']/a/@title").extract_first()
            item['book_desc'] = ul.xpath("./p[@class=''detail]/text()").extract_first()
            item['book_price'] = ul.xpath(".//span[@class='search_now_price']/text()").extract_first()
            item['book_author'] = ul.xpath("/p[@class='search_book_author']/span[1]/a/text()").extract()
            item['book_publish_data'] = ul.xpath("./p[@class='search_book_author']/span[2]/text()").extract_first()
            item['book_press'] = ul.xpath("./p[@class='search_book_author']/span[3]/a/text()").extract_first()
            print(item)
