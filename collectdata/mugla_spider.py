# -*-coding: utf-8 -*-
import scrapy
from tutorial.items import MuglaItem
from scrapy import log, Request


class muglaSpider(scrapy.Spider):
    name = "eksisozluk"
    allowed_domains = ["eksisozluk.com"]
    start_urls = [
        "https://eksisozluk.com/",
    ]

    def parse(self, response):
        universiteler = ["mugla sitki kocman universitesi",
                         "dokuz eylul universitesi","ege universitesi",
                         "gediz universitesi","izmir ekonomi universitesi","izmir katip celebi universitesi","izmir universitesi",
                         "turk hava kurumu universitesi","yasar universitesi","izmir yuksek teknoloji enstitusu","sifa universitesi"]  # uni isimlerini turkce karakter olarak gir,

        base_url = "https://eksisozluk.com/?q=%s" 
        for universite in universiteler:
            yield Request(base_url % universite, self.parse2)

    def parse2(self, response):  
        url = response.url
        for i in range(13):
            base_url = url.split('?')[0] + "?p=%s"
            yield Request(base_url % (i + 1), self.parse3)

    def parse3(self, response):
        item = MuglaItem()
        print("------------page=%s" % (response.url))
        schoolName=response.url.split('/')[3]
        sep = '--'
        schoolName = schoolName.split(sep, 1)[0]
        for i in response.css('ul#entry-list li'):
            comment = i.css(" div.content *::text").extract()
            if comment:
                item['comment'] = comment
                item['school']=schoolName
                yield item
