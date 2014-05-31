# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from herekitty import config
from herekitty.items import Pet
from scrapy.contrib.loader import ItemLoader
import json
import codecs
import time
import datetime

class PetSpider(Spider):
    name = "pet_spider"

    def __init__(self, category=None, *args, **kwargs):
        super(PetSpider, self).__init__(*args, **kwargs)
        self.query_list = config.QUERY.query_list()
        for query in self.query_list:
            self.start_urls.append(query[1])
        #self.start_urls = config.QUERY.query_list()
        self.query_count = 0

    def parse(self, response):
        self.current_time = time.clock()
        sel = Selector(response)
        results_table = sel.xpath('//td/text()').extract()
        #get images here
        results_table = results_table[1:]

        l = ItemLoader(item=Pet())
        master_list = []
        scrape_categories = config.SCRAPE_CATEGORIES
        discarded_categories = config.DISCARDED_CATEGORIES
        special_categories = config.SPECIAL_CATEGORIES
        for i, entry in enumerate(results_table):
            index = i % len(scrape_categories)
            if scrape_categories[index] in special_categories:
                res = config.SPECIAL_FUNCTIONS[scrape_categories[index]](entry)
                for result in res:
                    l.add_value(result["category"], result["value"])

            if scrape_categories[index] not in discarded_categories and scrape_categories[index] not in special_categories:
                l.add_value(scrape_categories[index], entry)
            if index == len(scrape_categories)-1:
                l.add_value("scraped_at", unicode(time.strftime("%Y-%m-%d %H:%M:%S")))
                master_list.append(l.load_item())
                l = ItemLoader(item=Pet())

        timestr = str(self.current_time)
        with codecs.open(timestr + 'spideroutput.txt', 'w', encoding='utf-8') as fout:
            fout.write('LENGTH: ' + str(len(master_list)) + '\n\n')
            fout.write(repr(master_list))

        #if self.query_count

        return
