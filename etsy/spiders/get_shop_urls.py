import datetime

import mysql
import scrapy
from scrapy.utils.sitemap import Sitemap


class GetShopUrlsSpider(scrapy.Spider):
    # Spider name
    name = 'get_shop_urls'
    my_db_connection = None

    def __init__(self, *args, **kwargs):
        self.connect_db()
        self.start_urls = ['https://www.etsy.com/dynamic-sitemaps.xml?sitemap=shop_index_2']
        super(GetShopUrlsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        s = Sitemap(response.body)

        if s.type == 'sitemapindex':
            for loc in s:
                yield scrapy.Request(loc['loc'], callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        s = Sitemap(response.body)
        items_to_save = []
        now = datetime.datetime.utcnow()
        if s.type == 'urlset':
            for loc in s:
                items_to_save.append((loc['loc'], 0, 'shop', now.strftime('%Y-%m-%d %H:%M:%S')))

            sql = "insert into urls (url,item_count, url_type, created_date)" \
                  "values(%s,%s,%s,%s)"
            mycursor = self.my_db_connection.cursor()
            mycursor.executemany(sql, items_to_save)
            self.my_db_connection.commit()


    def connect_db(self):
        self.my_db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            database='etsydb',
            password="1234"
        )
        print("DB INITIALIZED!")
