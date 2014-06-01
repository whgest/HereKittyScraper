# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from herekitty import config
from herekitty.items import Pet
from scrapy.contrib.loader import ItemLoader
import time

class PetSpider(Spider):
    name = "pet_spider"

    def __init__(self, category=None, *args, **kwargs):
        super(PetSpider, self).__init__(*args, **kwargs)
        self.query_list = config.QUERY.query_list()
        for query in self.query_list:
            self.start_urls.append(query[0])
        #self.start_urls = config.QUERY.query_list()
        self.query_count = 0
        self.final_database = []
        self.final_final_database = []
        self.scrapedat = unicode(time.strftime("%Y-%m-%d %H:%M:%S"))

    def parse(self, response):
        self.current_time = time.clock()
        sel = Selector(response)
        results_table = sel.xpath('//td/text()').extract()
        #get images here
        results_table = results_table[1:]


        l = ItemLoader(item=Pet())
        #pet = {}
        #l = Pet()
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
                    #l[result["category"]] = result["value"]
            if scrape_categories[index] not in discarded_categories and scrape_categories[index] not in special_categories:
                l.add_value(scrape_categories[index], entry)
                #pet[[scrape_categories[index]]] = entry
            if index == len(scrape_categories)-1:
                l.add_value("scraped_at", self.scrapedat)
                l.add_value("species", self.query_list[self.query_count][1]["atype"])
                #pet["scraped_at"] = self.scrapedat
                loaded_item = l.load_item()
                for key in loaded_item:
                    loaded_item[key] = loaded_item[key][0]
                master_list.append(loaded_item)
                l = ItemLoader(item=Pet())
                #l = Pet()


        # with codecs.open(timestr + 'spideroutput.txt', 'w', encoding='utf-8') as fout:
        #     fout.write('LENGTH: ' + str(len(master_list)) + '\n\n')
        #     fout.write(repr(master_list))

        # if self.query_list[self.query_count][1]["searchtype"] == "LOST":
        #     self.lost_database.extend(master_list)
        # elif self.query_list[self.query_count][1]["searchtype"] == "ADOPT":
        #     self.adopt_database.extend(master_list)

        self.final_database.extend(master_list[:-1])
        self.query_count += 1

        if self.query_count == 6:
            id_dupes = []
            for pet in self.final_database:
                if pet.get("pet_id") in id_dupes:
                    pass
                else:
                    self.final_final_database.append(pet)
                    id_dupes.append(pet.get("pet_id"))

            return self.final_final_database


