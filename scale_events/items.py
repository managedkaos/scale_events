import scrapy

class ScaleEventItem(scrapy.Item):
    speaker = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    time = scrapy.Field()
    room = scrapy.Field()
    topic = scrapy.Field()

