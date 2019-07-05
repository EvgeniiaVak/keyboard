# -*- coding: utf-8 -*-
import scrapy


class YandexMarketSpider(scrapy.Spider):
    name = 'yandex_market'
    allowed_domains = ['market.yandex.ru']
    start_urls = ['https://market.yandex.ru/catalog--klaviatury/68334/list/']
    custom_settings = {'FEED_FORMAT': 'csv', 'FEED_URI': 'yandex_market_%(time)s.csv'}

    def parse(self, response):

        # find the list of items on this page
        items = response.css(".n-snippet-list .n-snippet-cell2")

        # yield each item
        for item in items:
            yield {
                'title': item.css(".n-snippet-cell2__title .link::text").get(),
                'price': item.css(".n-snippet-cell2__main-price-wrapper .price::text").get(),
                'rating': item.css(".rating .rating__value::text").get(),
                'reviewed': item.css(".n-snippet-card2__rating span::text").get(),
                'advantages': item.css(".n-reason-to-buy__best-item::text").getall()
            }

        # go to next page if one exists
        next_page = response.css('.n-pager__button-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)
