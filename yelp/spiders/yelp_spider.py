from scrapy import Spider, Request
from yelp.items import YelpItem
import re


class YelpSpider(Spider):

    name = 'yelp_spider'
    allowed_urls = ['https://www.yelp.com/']

    # cuisines = ['japanese', 'mexican', 'american', 'italian', 'thai', 'chinese', 'mediterranean']
    # locations = ['San%20Francisco%2C%20CA','New%20York%2C%20NY', 'Austin%2C%20TX']
    # start_urls = [f'https://www.yelp.com/search?find_desc={cuisine}&find_loc={location}&ns=1&start=0' for location in locations for cuisine in cuisines]

    start_urls = ['https://www.yelp.com/search?find_desc=japanese&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=mexican&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=american&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=italian&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=thai&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=chinese&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=mediterranean&find_loc=San%20Francisco%2C%20CA&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=japanese&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=mexican&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=american&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=italian&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=thai&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=chinese&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=mediterranean&find_loc=New%20York%2C%20NY&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=japanese&find_loc=Austin%2C%20TX&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=mexican&find_loc=Austin%2C%20TX&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=american&find_loc=Austin%2C%20TX&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=italian&find_loc=Austin%2C%20TX&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=thai&find_loc=Austin%2C%20TX&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=chinese&find_loc=Austin%2C%20TX&ns=1&start=0',
                 'https://www.yelp.com/search?find_desc=mediterranean&find_loc=Austin%2C%20TX&ns=1&start=0']



    def parse(self, response):

        # Find cuisine and location regex - return normal name 

        # cuisine = re.findall('find_desc=([^&]+)', response.url)[0].replace('%20', ' ')
        # location = re.findall('find_loc=([^&]+)', response.url)[0].replace('%20', ' ').replace('%2C', ',')

        # meta = {'cuisine':cuisine, 'location':location}

        num_pages = response.xpath('//div[@class="lemon--div__373c0__1mboc border-color--default__373c0__3-ifU text-align--center__373c0__2n2yQ"]/span/text()').extract_first()
        print("Page: " + num_pages)
        pattern = re.search('1 of (\d+)', num_pages)

        print(pattern)
        print(pattern.group(0))
        print(pattern.group(1))
        num_pages = int(re.search('1 of (\d+)', num_pages).group(1))

        # url_list = [f'https://www.yelp.com/search?find_desc=japanese%20food&find_loc=San%20Francisco%2C%20CA&ns=1&start={i*30}' for i in range(num_pages)]
        url_list = []

        for url in self.start_urls:
            url = url[:-1]
            for i in range(num_pages):
                url_list.append(url + str(i*30))


        for url in url_list:
            cuisine = re.search('find_desc=([^&]+)', url).group(1).replace('%20', ' ')
            location = re.search('find_loc=([^&]+)', url).group(1).replace('%20', ' ').replace('%2C', ',')
            meta = {'cuisine': cuisine, 'location': location}

            yield Request(url=url, callback=self.parse_results_page, meta=meta)



    def parse_results_page(self, response):
        business_urls = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-regular__373c0__2vGEn text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--inherit__373c0__2fB3p"]/a/@href').extract()
        business_urls = business_urls[1:]
        business_urls = [f'https://www.yelp.com{suffix}&sort_by=date_desc' for suffix in business_urls]


        for url in business_urls:
            response.meta['url'] = url
            yield Request(url=url, callback=self.parse_business_page, meta=response.meta)

    # def parse_covid_services(response, meta):
    #     dict = {}
    #     for x in response.xpath('//div[@class="lemon--div__373c0__1mboc margin-t2__373c0__1CFWK border-color--default__373c0__3-ifU"]//div[@class="lemon--div__373c0__1mboc display--inline-block__373c0__1ZKqC margin-r3__373c0__r37sx margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]').getall(): 
    #         service = re.search('<span.*?text.*?([A-Za-z\s\-]*)<\/span',x)
    #         if service != None:
    #             dict[service.group(1)] = re.search("checkmark",x) != None
    #     return dict

    def parse_business_page(self, response):
        restaurant_name = response.xpath('//h1[@class="lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy"]/text()').extract_first()

        try:
            avg_rating = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange__373c0__2C9bH gutter-1-5__373c0__2vL-3 vertical-align-middle__373c0__1SDTo margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]/div/span/div/@aria-label').extract_first()
            avg_rating = float(re.findall('(\d?\.?\d) star rating', avg_rating)[0])
        except:
            avg_rating = None
            print('='*50)
            print(f'Error with avg_rating at url: {response.url}')
            print('='*50)

        try:
            num_reviews = response.xpath('//p[@class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa- text-size--large__373c0__3t60B"]/text()').extract_first()
            num_reviews = int(re.findall('(\d+) review[s]?', num_reviews)[0])
        except:
            num_reviews = 0
            print('='*50)
            print(f'Error with num_reviews at url: {response.url}')
            print('='*50)

        phone_num = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange__373c0__2C9bH gutter-2__373c0__1DiLQ vertical-align-middle__373c0__1SDTo border-color--default__373c0__3-ifU"]//p[@class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-"]/text()').extract_first()

        address = response.xpath('//address[@class="lemon--address__373c0__2sPac"]//span/text()').extract()
        address = ', '.join(address)

        days = response.xpath('//table[@class="lemon--table__373c0__2clZZ hours-table__373c0__1S9Q_ table__373c0__3JVzr table--simple__373c0__3lyDA"]//tr')
        hours_dict = {day.xpath('./th/p/text()').extract_first():day.xpath('./td/ul/li/p/text()').extract_first() for day in days}


        # for day in days:
        #     key = day.xpath('./th/p/text()').extract_first()
        #     value = day.xpath('./td/ul/li/p/text()').extract_first()
        #     hours_dict[key] = value

        price_range = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B"]/text()').extract_first()
        
        category = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa- text-size--large__373c0__3t60B"]/a/text()').extract()


        # This return a list of all review ratings in the first review page , some problems
        # review_rating = response.xpath('//div[@class="lemon--div__373c0__1mboc arrange__373c0__2C9bH gutter-1__373c0__2l5bx vertical-align-middle__373c0__1SDTo border-color--default__373c0__3-ifU"]/div/span/div/@aria-label').extract()[:20]
        review_rating = response.xpath('//div[@class="lemon--div__373c0__1mboc margin-t1__373c0__oLmO6 margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]/div/div/span/div/@aria-label').extract()
        review_rating = review_rating[:-1] # Drop the last review which is not chronological 

        review_date = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-"]/text()').extract()
        review_date = review_date[:-1] # Drop the last review which is not chronological 

        # review_user = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz fs-block text-color--blue-dark__373c0__1jX7S text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz"]/a/text()').extract()

        recent_reviews = list(zip(review_rating, review_date))


        covid_updates_text = response.xpath('//div[@class="lemon--div__373c0__1mboc margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]//p/text()').extract_first()

        covid_update_time = response.xpath('//p[@class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--subtle__373c0__3DZpi text-align--left__373c0__2XGa-"]/text()').extract_first()


        pairs = response.xpath('//span[@class="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-size--large__373c0__3t60B"]/text()').extract()

        covid_services = {}
        for x in response.xpath('//div[@class="lemon--div__373c0__1mboc margin-t2__373c0__1CFWK border-color--default__373c0__3-ifU"]//div[@class="lemon--div__373c0__1mboc display--inline-block__373c0__1ZKqC margin-r3__373c0__r37sx margin-b1__373c0__1khoT border-color--default__373c0__3-ifU"]').getall(): 
            service = re.search('<span.*?text.*?([A-Za-z\s\-]*)<\/span',x)
            if service != None:
                covid_services[service.group(1)] = re.search("checkmark",x) != None


        item = YelpItem()
        item['restaurant_name'] = restaurant_name
        item['avg_rating'] = avg_rating
        item['num_reviews'] = num_reviews
        item['phone_num'] = phone_num
        item['address'] = address
        item['business_hours'] = hours_dict
        item['price_range'] = price_range
        item['category'] = category
        item['recent_reviews'] = recent_reviews

        item['covid_updates_text'] = covid_updates_text
        item['covid_update_time'] = covid_update_time
        item['covid_services'] = covid_services

        item['location'] = response.meta['location']
        item['cuisine'] = response.meta['cuisine']
        item['url'] = response.meta['url']

        yield item




# For COVID Section dictionary
# Find each key/value pair div as a Selector list 


# pairs = response.xpath('//div[@class="lemon--div__373c0__1mboc margin-t2__373c0__1CFWK border-color--default__373c0__3-ifU"]/div')

# covid_dict = {}
# for pair in pairs:
#   key = pair.xpath('./span/text()')
#   value = bool(pair.xpath('./div/span[contains(@class,"checkmark")'))
#   covid_dict[key] = value

# item['outdoor_seating'] = covid_dict.get('Outdoor Seating')













