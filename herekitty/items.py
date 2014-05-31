# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Pet(Item):
    species = Field()
    pet_ID = Field()
    name = Field()
    gender = Field()
    fixed = Field()
    color = Field()
    breed = Field()
    shelter_name = Field()
    found_on = Field()
    scraped_at = Field()
    status = Field()
