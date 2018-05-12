# -*- coding: utf-8 -*-

import json
import random

import scrapy
from scrapy.utils.project import get_project_settings


class DiseaseDetailSpider(scrapy.Spider):
    name = "disease_detail"
    host = 'http://ypk.39.net'
    referer = 'http://ypk.39.net/allcategory'
    USER_AGENTS = get_project_settings().get('USER_AGENTS')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('disease.json') as disease_file:
            self.data = json.load(disease_file)

        self.crawled = set()
        try:
            with open('disease_detail.jl') as file:
                for line in file:
                    crawled_data = json.loads(line)
                    for name in crawled_data:
                        self.crawled.add(name)
        except FileNotFoundError:
            pass

        print(self.crawled)

    def start_requests(self):
        for d_ in self.data:
            for category in d_:
                for disease, url in d_[category].items():
                    if disease in self.crawled or not url:
                        continue
                    self.crawled.add(disease)
                    yield scrapy.Request(url=url, callback=self.parse, headers={
                        'Referer': self.referer,
                        'User-Agent': random.choice(self.USER_AGENTS),
                    })

    def parse(self, response):
        name = response.css('h2.label_title::text').extract_first()
        info = response.css('h2.label_title a::attr(href)').extract_first()
        med_path = response.css('div.label_ypsz_box .content p.name a::attr(href)').extract()
        med_name = response.css('div.label_ypsz_box .content p.name a::text').extract()

        # 防止被反爬虫
        if not med_name:
            pass
            # yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True, headers={
            #     'Referer': self.referer,
            #     'User-Agent': random.choice(self.USER_AGENTS),
            # })
        else:
            yield {
                name: {
                    'info': info,
                    'meds': {
                        n: self.host + p for n, p in zip(med_name, med_path)
                    }
                }
            }
