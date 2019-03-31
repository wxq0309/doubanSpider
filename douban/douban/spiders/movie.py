# -*- coding: utf-8 -*-
import json, random

import scrapy
from scrapy import Request, FormRequest

from douban import settings
from ..items import DoubannowplayingItem, DoubanUpcomingItem, DoubanlistwpItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    # start_urls = ['https://movie.douban.com/chart']
    nowplaying_url = 'https://movie.douban.com/cinema/nowplaying/{area}'
    area = 'jinzhong'
    upcoming_url = 'https://movie.douban.com/coming'
    login_url = 'https://accounts.douban.com/passport/login'
    index_url = 'https://www.douban.com'
    top_url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={start}'
    # cookie = settings['COOKIE']
    data = {
        "name": '18734422941',
        "password": 'fengshan',
    }
    cookie = random.choice(settings.COOKIE)
    print("================================")
    print(cookie)
    print("================================")

    def start_requests(self):
        # yield Request(self.index_url, meta={'cookiejar': 1}, callback=self.parse_login)
        yield Request(self.nowplaying_url.format(area=self.area), self.parse_nowplaying, cookies=self.cookie)
        yield Request(self.upcoming_url, self.parse_upcoming, cookies=self.cookie)
        for a in range(0, 21, 20):
            yield Request(self.top_url.format(start=a), self.parse_top_movie, cookies=self.cookie)

    def parse_login(self, response):
        # print(response.status)
        return FormRequest(
            url=self.login_url,
            formdata=self.data,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_after_login,
        )

    def parse_after_login(self, response):
        print("=========================================")
        print(response.status)

    # 正在上映电影列表
    def parse_nowplaying(self, response):
        item = DoubannowplayingItem()
        li_list = response.xpath("//div[@id='nowplaying']/div[2]/ul/li")
        for li in li_list:
            item['image_url'] = li.xpath(".//img/@src").extract_first()
            item['title'] = li.xpath("./@data-title").extract_first()
            item['score'] = li.xpath("./@data-score").extract_first()
            item['release'] = li.xpath("./@data-release").extract_first()
            item['duration'] = li.xpath("./@data-duration").extract_first()
            item['region'] = li.xpath("./@data-region").extract_first()
            item['director'] = li.xpath("./@data-director").extract_first()
            item['actors'] = ','.join([i for i in
                                       ','.join([actors for actors in li.xpath("./@data-actors").extract()]).replace(
                                           '/', '').split()])

            item['detail_url'] = li.xpath(".//li[@class='poster']/a/@href").extract_first()

            yield Request(
                url=item['detail_url'],
                callback=self.parse_nowplaying_detail,
                meta={'item': item}
            )

    def parse_nowplaying_detail(self, response):
        item = response.meta['item']
        item['desc'] = \
            ''.join([i.strip() for i in response.xpath("//div[@class='indent']//text()").extract()]).replace('\n',
                                                                                                             '').split()[
                0]

        item['hot_comments'] = ''.join([i.strip() for i in response.xpath(
            "//div[@id='hot-comments']/div[@class='comment-item'][1]//p//text()").extract()]).replace('\n', '').split()[
            0]
        yield item
        # print(item)

    # 即将上映电影列表
    def parse_upcoming(self, response):
        item = DoubanUpcomingItem()
        tr_list = response.xpath("//table[@class='coming_list']/tbody//tr")
        for tr in tr_list:
            item['upcoming_release_time'] = tr.xpath("./td[1]/text()").extract_first().strip().replace('\n', '')
            item['upcoming_title'] = tr.xpath("./td[2]/a/text()").extract_first().strip().replace('\n', '')
            item['upcoming_kind'] = tr.xpath("./td[3]/text()").extract_first().strip().replace('\n', '')
            item['upcoming_area'] = tr.xpath("./td[4]/text()").extract_first().strip().replace('\n', '')
            item['upcoming_love_num'] = tr.xpath("./td[5]/text()").extract_first().strip().replace('\n', '')
            # print(item)
            yield item

    # 电影榜单 按评分排序
    def parse_top_movie(self, response):
        result = json.loads(response.text)
        # print(result)
        i = 0
        item = DoubanlistwpItem()
        for content in result['data']:
            i += 1
            item['list_rank'] = i
            item['list_directors'] = content['directors'] if len(content['directors']) > 0 else None
            if item['list_directors'] != None:
                item['list_directors'] = ','.join([i for i in item['list_directors']])
            item['list_cover'] = content['cover']
            item['list_title'] = content['title']
            item['list_rate'] = content['rate']
            item['list_url'] = content['url']
            item['list_casts'] = ','.join([i.strip() for i in content['casts']])

            yield Request(
                url=item['list_url'],
                callback=self.parse_desc,
                meta={'item': item}
            )

    def parse_desc(self, response):
        item = response.meta['item']
        item['list_desc'] = ','.join(
            [i.strip() for i in response.xpath("//div[@id='link-report']//text()").extract()]).replace('\n', '')
        yield item
        # print(item)
