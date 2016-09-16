from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ypextract.items import YpextractItem
from scrapy import log

class YpSpider(BaseSpider):
	name = "yellowpages"
	allowed_domains = ["yellowpages.com"]
	start_urls = ["http://www.yellowpages.com/houston-tx/mip/houston-methodist-willowbrook-hospital-7482379"]
	start_urls.append("http://www.yellowpages.com/houston-tx/mip/houston-methodist-willowbrook-hospital-7482379?page=2")
	#manually insert all links that are wanted here:
	start_urls.append("http://www.yellowpages.com/houston-tx/mip/houston-methodist-st-john-hospital-457886484")
	start_urls.append("http://www.yellowpages.com/houston-tx/mip/houston-methodist-west-hospital-465261435")
	for i in range(1,3):
		start_urls.append("http://www.yellowpages.com/sugar-land-tx/mip/houston-methodist-sugar-land-hospital-2716514?page=" + str(i))
	start_urls.append("http://www.yellowpages.com/katy-tx/mip/houston-methodist-st-catherine-hospital-455673804")
	start_urls.append("http://www.yellowpages.com/baytown-tx/mip/san-jacinto-methodist-hospital-4315599")

	def parse(self, response):
		sel = Selector(response)
		dataset = sel.xpath('//div[@itemprop="review"]')
		datastruct = []
		for data in dataset:
			item = YpextractItem()
			item['location'] = sel.xpath('//h1[@itemprop="name"]/text()').extract()
			item['rating'] = data.xpath('.//div[@itemprop="reviewRating"]/div/meta/@content').extract()
			tp = data.xpath('.//span[@class="truncated"]')
			if not tp:
				item['review'] = data.xpath('.//p[@itemprop="reviewBody"]/text()').extract()
			else:
				tp = data.xpath('.//span[@class="truncated"]/text()').extract()
				tp2 = data.xpath('.//span[@class="restoftext hide"]/text()').extract()
				item['review'] = tp + tp2
			datastruct.append(item)
		return datastruct
