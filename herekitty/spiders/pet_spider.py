from scrapy.spider import Spider
from scrapy.selector import Selector
from herekitty import config
from herekitty.items import Pet
from scrapy.contrib.loader import ItemLoader
import codecs

class PetSpider(Spider):
    name = "pet_spider"

    def __init__(self, category=None, *args, **kwargs):
        super(PetSpider, self).__init__(*args, **kwargs)
        self.start_urls = [config.QUERY.generate_URL()]

    def parse(self, response):
        sel = Selector(response)
        results_table = sel.xpath('//td/text()').extract()
        results_table = results_table[1:]

        l = ItemLoader(item=Pet())
        master_list = []
        categories = ['ID', 'gender', 'color', 'breed',
                      'age_years', 'age_months', 'age_days', 'found', 'location']
        for i, entry in enumerate(results_table):
            index = i % 9
            l.add_value(categories[index], entry)
            if index == 8:
                master_list.append(l.load_item())
                l = ItemLoader(item=Pet())

        with codecs.open('spideroutput.txt', 'w', encoding='utf-8') as fout:
            fout.write('LENGTH: ' + str(len(master_list)) + '\n\n')
            fout.write(repr(master_list))

        print results_table
        return
