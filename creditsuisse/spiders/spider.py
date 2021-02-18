import scrapy

from scrapy.loader import ItemLoader
from ..items import CreditsuisseItem
from itemloaders.processors import TakeFirst


class CreditsuisseSpider(scrapy.Spider):
	name = 'creditsuisse'
	start_urls = ['https://www.credit-suisse.com/about-us/en/media-news/media-releases.html']

	def parse(self, response):
		post_links = response.xpath('//article')
		for post in post_links:
			url = post.xpath('.//a[@class="a-link"]/@href').get()
			date = post.xpath('.//article/div[@class="m-article-listing__date"]//text()[normalize-space()]').getall()
			if url[-3:] != 'pdf':
				yield response.follow(url, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="mod_media_release_title"]/text()').get()
		description = response.xpath('//div[@class="mod_page_abstract"]//text()|//div[@class="mod_table_footnotes"]//text()|//div[@class="component_standard"]/div/div/p//text()|//aside//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath("//time/text()").get()

		item = ItemLoader(item=CreditsuisseItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
