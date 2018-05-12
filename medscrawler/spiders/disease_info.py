# -*- coding: utf-8 -*-

import json
import random

import scrapy
from scrapy.utils.project import get_project_settings


class DiseaseInfoSpider(scrapy.Spider):
    name = "disease_info"
    host = 'http://ypk.39.net'
    referer = 'http://ypk.39.net/allcategory'
    USER_AGENTS = get_project_settings().get('USER_AGENTS')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        with open('disease_detail.jl') as file:
            for line in file:
                self.data.append(json.loads(line))

        self.crawled = set()
        try:
            with open('disease_info.jl') as file:
                for line in file:
                    crawled_data = json.loads(line)
                    for name in crawled_data:
                        self.crawled.add(name)
        except FileNotFoundError:
            pass

        print(self.crawled)

    def start_requests(self):
        for d_ in self.data:
            for disease in d_:
                if disease in self.crawled:
                    continue
                self.crawled.add(disease)
                url = d_[disease]['info']
                if not url:
                    continue
                yield scrapy.Request(url=url, callback=self.parse, headers={
                    'Referer': self.referer,
                    'User-Agent': random.choice(self.USER_AGENTS),
                })

    def parse(self, response):
        disease = response.css('dl.intro dt::text').extract_first()
        raw = response.css('.info ul li > *:not(cite)::text ,.info ul li::text').extract()
        trimmed = [r_.strip() for r_ in raw if r_.strip()]

        # 解析 infobox
        parsed = {}
        i = 0
        while i < len(trimmed):
            c_ = trimmed[i]
            if c_.endswith('：'):
                l_ = []
                i += 1
                while i < len(trimmed) and not trimmed[i].endswith('：'):
                    l_.append(trimmed[i])
                    i += 1
                l_ = l_ or ['']
                parsed[c_[:-1]] = l_ if len(l_) > 1 else l_.pop()

        # 防止被反爬虫
        if not trimmed:
            pass
            # yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True, headers={
            #     'Referer': self.referer,
            #     'User-Agent': random.choice(self.USER_AGENTS),
            # })
        else:
            yield {
                disease: parsed
            }
