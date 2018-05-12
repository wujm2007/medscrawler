# -*- coding: utf-8 -*-

import json
import random

import scrapy
from scrapy.utils.project import get_project_settings


class MedsInfoSpider(scrapy.Spider):
    name = "meds_info"
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
            with open('meds_info.jl') as meds_info_file:
                for line in meds_info_file:
                    crawled_data = json.loads(line)
                    for name in crawled_data:
                        self.crawled.add(name)
        except FileNotFoundError:
            pass

        print(self.crawled)

    def start_requests(self):
        for d_ in self.data:
            for disease in d_:
                meds = d_[disease]['meds']
                for m_, u_ in meds.items():
                    if m_ in self.crawled or not u_:
                        continue
                    self.crawled.add(m_)
                    yield scrapy.Request(url=u_ + 'manual', callback=self.parse, headers={
                        'Referer': self.referer,
                        'User-Agent': random.choice(self.USER_AGENTS),
                    })

    def parse(self, response):
        med = response.css('.t1 h1 a::text').extract_first()
        raw = response.css('div.tab_box div dl dt::text, div.tab_box div dl dd::text,'
                           ' div.tab_box div dl p::text, div.tab_box div dl a::text').extract()

        # 适应症特殊处理
        trimmed = [r_.strip() if not '适应症' in r_.strip() else '【适应症】' for r_ in raw if r_.strip()]

        # 解析 infobox
        parsed = {}
        i = 0
        while i < len(trimmed):
            c_ = trimmed[i]
            if c_.endswith('】'):
                l_ = []
                i += 1
                while i < len(trimmed) and not trimmed[i].endswith('】'):
                    l_.append(trimmed[i])
                    i += 1
                parsed[c_[1:-1]] = "\n".join(l_)

        print(parsed)

        # 防止被反爬虫
        if not trimmed:
            pass
            # yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True, headers={
            #     'Referer': self.referer,
            #     'User-Agent': random.choice(self.USER_AGENTS),
            # })
        else:
            yield {
                med: parsed
            }
