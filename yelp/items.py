# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    restaurant_name = scrapy.Field()
    avg_rating = scrapy.Field()
    num_reviews = scrapy.Field()
    price_range = scrapy.Field()
    category = scrapy.Field()

    phone_num = scrapy.Field()
    address = scrapy.Field()

    business_hours = scrapy.Field()

    # review_user = scrapy.Field()
    # review_date = scrapy.Field()
    # review_rating = scrapy.Field()
    recent_reviews = scrapy.Field()

    covid_updates_text = scrapy.Field()
    covid_update_time = scrapy.Field()
    covid_services = scrapy.Field()

    location = scrapy.Field()
    cuisine = scrapy.Field()
    url = scrapy.Field()

    #covid_updates_service = scrapy.Field()
    #covid_updates_health = scrapy.Field()
    # Amenities = scrapy.Field()


    