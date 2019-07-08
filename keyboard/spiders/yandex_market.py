# -*- coding: utf-8 -*-
import scrapy


class YandexMarketSpider(scrapy.Spider):
    name = 'yandex_market'
    allowed_domains = ['market.yandex.ru']
    start_urls = ['https://market.yandex.ru/catalog--klaviatury/68334/list/']
    custom_settings = {'FEED_FORMAT': 'csv', 'FEED_URI': 'data/yandex_market_%(time)s.csv'}

    def parse(self, response):

        # find the list of items on this page
        items = response.css(".n-snippet-list .n-snippet-cell2")

        # yield each item
        for item in items:
            yield {
                'title': item.css(".n-snippet-cell2__title .link::text").get().replace("Клавиатура", "").strip(),
                'price': item.css(".n-snippet-cell2__main-price-wrapper .price::text").re_first(r"[0-9]+.?[[0-9]+]?"),
                'rating': item.css(".rating .rating__value::text").get(),

                # number of reviews
                'reviewed': item.css(".n-snippet-card2__rating span::text").re_first(r"[0-9]+"),
                'advantages': item.css(".n-reason-to-buy__best-item::text").getall()
            }

        # go to next page if one exists
        next_page = response.css('.n-pager__button-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)
