from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from yelpextract.items import YelpextractItem

class YelpSpider(BaseSpider):
	name = "yelp"
	allowed_domains = ["yelp.com"]
	start_urls = ["http://www.yelp.com/biz/houston-methodist-hospital-houston"]
	for i in range(1,3):
		start_urls.append("http://www.yelp.com/biz/houston-methodist-hospital-houston?start=" + str(i*20))
	start_urls.append("http://www.yelp.com/biz/san-jacinto-methodist-hospital-baytown-4")
	for i in range(1,3):
		start_urls.append("http://www.yelp.com/biz/houston-methodist-willowbrook-hospital-houston?start=" + str((i-1)*20))
	start_urls.append("http://www.yelp.com/biz/houston-methodist-st-john-hospital-nassau-bay")
	for i in range(1,4):
		start_urls.append("http://www.yelp.com/biz/houston-methodist-west-hospital-houston?start=" + str((i-1)*20))
	for i in range(1,3):
		start_urls.append("http://www.yelp.com/biz/methodist-sugar-land-hospital-sugar-land?start=" + str((i-1)*20))

	def parse(self, response):
		sel = Selector(response)
		titles = sel.xpath('//div[@class="review-content"]')
		items = []
		for titles in titles:
			item = YelpextractItem()
			item['location'] = sel.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()
			item['review'] = titles.xpath("p/text()").extract()
			item['rating'] = titles.xpath("div/div/div/meta/@content").extract()
			items.append(item)
		return items
