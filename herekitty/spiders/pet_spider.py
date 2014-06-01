# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from herekitty import config
from herekitty.items import Pet
from scrapy.contrib.loader import ItemLoader
import time
import os


class PetSpider(Spider):
    """
    Scrape pet harbor search and export to json. Run spider from terminal:

    scrapy crawl pet_spider -o spider_data.json -t json

    """
    name = "pet_spider"

    def __init__(self, category=None, *args, **kwargs):
        super(PetSpider, self).__init__(*args, **kwargs)
        self.query_list = config.QUERY.query_list()
        for query in self.query_list:
            self.start_urls.append(query[0])
            print "QUERIES:", self.start_urls
        self.adopt_hash = {}
        self.lost_hash = {}
        self.query_count = 0
        self.all_pets = []
        self.loaded_models = []
        self.scraped_at = unicode(time.strftime("%Y-%m-%d %H:%M:%S"))
        try:
            os.remove('spider_data.json')
        except:
            pass

    def parse(self, response):
        url = response.url
        sel = Selector(response)
        results_table = sel.xpath('//td/text()').extract()
        results_table = results_table[1:]
        pet = {}
        master_dict = {}
        scrape_categories = config.SCRAPE_CATEGORIES
        discarded_categories = config.DISCARDED_CATEGORIES
        special_categories = config.SPECIAL_CATEGORIES
        for i, entry in enumerate(results_table):
            index = i % len(scrape_categories)
            if scrape_categories[index] in special_categories:
                res = config.SPECIAL_FUNCTIONS[scrape_categories[index]](entry)
                for result in res:
                    pet[result["category"]] = result["value"]
            if scrape_categories[index] not in discarded_categories and scrape_categories[index] not in special_categories:
                pet[scrape_categories[index]] = entry
            if index == len(scrape_categories)-1:
                pet["scraped_at"] = self.scraped_at
                if u"atype=cat" in url:
                    pet["species"] = u"cat"
                elif u"atype=dog" in url:
                    pet["species"] = u"dog"
                else:
                    pet["species"] = u"other"
                master_dict[pet["pet_id"]] = pet
                pet = {}

        if u"LOST" in url:
            self.lost_hash.update(master_dict)
        elif u"ADOPT" in url:
            self.adopt_hash.update(master_dict)

        self.query_count += 1

        if self.query_count == len(config.QUERIES):

            all_ids = self.adopt_hash.keys()
            all_ids.extend(self.lost_hash.keys())
            for id in all_ids:
                if id in self.adopt_hash and id in self.lost_hash:
                    self.adopt_hash[id]["status"] = u"BOTH"
                    del self.lost_hash[id]
                    self.all_pets.append(self.adopt_hash[id])
                    del self.adopt_hash[id]
                elif id in self.adopt_hash:
                    self.adopt_hash[id]["status"] = u"ADOPT"
                    self.all_pets.append(self.adopt_hash[id])
                    del self.adopt_hash[id]
                elif id in self.lost_hash:
                    self.lost_hash[id]["status"] = u"LOST"
                    self.all_pets.append(self.lost_hash[id])
                    del self.lost_hash[id]

            for pet in self.all_pets:
                l = ItemLoader(item=Pet())
                for key in pet:
                    l.add_value(key, pet[key])
                loadeditem = l.load_item()
                for key in loadeditem:
                    loadeditem[key] = loadeditem[key][0]
                if loadeditem.get("pet_id") != " ":
                    self.loaded_models.append(loadeditem)
            return self.loaded_models

