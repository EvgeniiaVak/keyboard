# -*- coding: utf-8 -*-
import scrapy


class YandexMarketSpider(scrapy.Spider):
    name = 'yandex_market'
    allowed_domains = ['market.yandex.ru']
    start_urls = ['https://market.yandex.ru/catalog--klaviatury/68334/list/']
    custom_settings = {'FEED_FORMAT': 'csv', 'FEED_URI': 'yandex_market_%(time)s.csv'}

    def parse(self, response):

        titles = response.css(".n-snippet-list .n-snippet-cell2__title .link::text").extract()
        prices = response.css(".n-snippet-cell2__main-price-wrapper .price::text").extract()
        ratings = response.css(".rating .rating__value::text").extract()
        reviews_number = response.css(".n-snippet-card2__rating span::text").extract()

        rows = zip(titles, prices, ratings, reviews_number)

        for row in rows:
            yield {
                'title': row[0],
                'price': row[1],
                'rating': row[2],
                'reviewed': row[3]
            }

        # go to next page if one exists
        next_page = response.css('.n-pager__button-next::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)
