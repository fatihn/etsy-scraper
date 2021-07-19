import datetime

import mysql.connector
import scrapy
from scrapy.utils.sitemap import Sitemap


# Spider Class
class GetCategoryUrlsSpider(scrapy.Spider):
    # Spider name
    name = 'get_category_urls'
    my_db_connection = None

    def __init__(self, *args, **kwargs):
        self.connect_db()
        self.start_urls = ['https://www.etsy.com/dynamic-sitemaps.xml?sitemap=taxonomyindex']
        super(GetCategoryUrlsSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        s = Sitemap(response.body)

        if s.type == 'sitemapindex':
            for loc in s:
                yield scrapy.Request(loc['loc'], callback=self.parse_sitemap)
        elif s.type == 'urlset':
            for loc in s:
                meta_data = {'sitemap_url': response.url}
                yield scrapy.Request(loc['loc'], meta=meta_data, callback=self.parse_category_page)

    def parse_sitemap(self, response):
        s = Sitemap(response.body)
        if s.type == 'urlset':
            for loc in s:
                meta_data = {'sitemap_url': response.url}
                yield scrapy.Request(loc['loc'], meta=meta_data, callback=self.parse_category_page)

    def parse_category_page(self, response):
        listing_count = 0
        if response.xpath('//span[contains(text(), "esult")]/text()'):
            tmp = response.xpath('//span[contains(text(), "esult")]/text()').extract_first()
            tmp = tmp.strip().replace("\n","")
            tmp = tmp.replace("(", "")
            tmp = tmp.replace(")", "")
            tmp = tmp.split(" ")[0]
            listing_count = tmp.replace("," , "")

        self.insert_url(response.url,'category', listing_count)


    def insert_url(self, url:str, url_type, listing_count):
        now = datetime.datetime.utcnow()
        sql = "insert into category (url,item_count, created_date)" \
              "values(%s,%s,%s)"
        val = (url, listing_count, now.strftime('%Y-%m-%d %H:%M:%S'))
        self.execute_stmt(sql, val)

    def connect_db(self):
        self.my_db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            database='etsydb',
            password="1234"
        )

    def execute_stmt(self, stmt: str, vals):
        mycursor = self.my_db_connection.cursor()
        mycursor.execute(stmt, vals)
        self.my_db_connection.commit()
        return mycursor.lastrowid
