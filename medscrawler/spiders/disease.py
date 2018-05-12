# -*- coding: utf-8 -*-

import random

import scrapy
from scrapy.utils.project import get_project_settings


class DiseaseSpider(scrapy.Spider):
    name = "disease"
    host = 'http://ypk.39.net'
    referer = 'http://ypk.39.net/allcategory'
    USER_AGENTS = get_project_settings().get('USER_AGENTS')

    def start_requests(self):
        urls = [
            self.host + path for path in [
                '/jbk/neike.html',
                '/jbk/waike.html',
                '/jbk/fuchanke.html',
                '/jbk/nanke.html',
                '/jbk/erke.html',
                '/jbk/ganbing.html',
                '/jbk/jingshenxinlike.html',
                '/jbk/chuanranke.html',
                '/jbk/pifuxingbing.html',
                '/jbk/shengzhijiankang.html',
                '/jbk/wuguanke.html',
                '/jbk/zhongyike.html',
                '/jbk/zhongliuke.html',
                '/jbk/yingyangke.html']
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={
                'Referer': self.referer,
                'User-Agent': random.choice(self.USER_AGENTS),
            })

    def parse(self, response):
        title = response.css('div.subs p strong::text').extract_first()
        keys = response.css('.types div.typecon ul li a::text').extract()
        paths = response.css('.types div.typecon ul li a::attr(href)').extract()

        # 重新请求，防止被反爬虫规则命中而缺少该条数据
        if not keys:
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True, headers={
                'Referer': self.referer,
                'User-Agent': random.choice(self.USER_AGENTS),
            })
        else:
            yield {
                title: {
                    k: self.host + p for k, p in zip(keys, paths)
                }
            }

