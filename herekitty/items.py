# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Pet(Item):
    species = Field()
    ID = Field()
    gender = Field()
    color = Field()
    breed = Field()
    age_years = Field()
    age_months = Field()
    age_days = Field()
    found = Field()
    location = Field()
