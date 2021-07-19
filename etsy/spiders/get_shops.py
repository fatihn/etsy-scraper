import datetime

import mysql.connector
import scrapy


# Spider Class
class GetShopsSpider(scrapy.Spider):
    # Spider name
    name = 'get_shops'
    allowed_domains = ['etsy.com']
    start_urls = ['https://www.etsy.com/']

    # Max number of items 
    COUNT_MAX = 10
    # Count the number of items scraped
    COUNTER = 0
    my_db_connection = None

    def __init__(self, *args, **kwargs):
        # Build the search URL
        self.connect_db()
        sql = "select url from urls where url_type = %s limit %s, %s"
        val = ('shop',0, 50000)
        ret = self.get_all_rows(sql, val)

        urls = []
        for r in ret:
            urls.append(r[0])

        self.start_urls = urls
        super(GetShopsSpider, self).__init__(*args, **kwargs)


    def parse(self, response):

        shop_url = response.url
        shop_id = ""
        shop_location = ""
        shop_on_etsy_since = ""
        shop_favorers = "0"
        shop_sold = "0"
        shop_rating = "0"
        shop_anouncement = ""
        shop_cover_photo = ""
        review_count = 0

        if response is None:
            now = datetime.datetime.utcnow()
            sql = "update urls set status = %s, crawl_time=%s, crawl_detail=%s where url = %s"
            val = ('ERROR', now.strftime('%Y-%m-%d %H:%M:%S'),'response is empty', response.url)
            self.execute_stmt(sql, val)
            return
        if response.status != 200:
            now = datetime.datetime.utcnow()
            sql = "update urls set status = %s, crawl_time=%s, crawl_detail=%s where url = %s"
            val = ('ERROR-'+response.status, now.strftime('%Y-%m-%d %H:%M:%S'), response.status, response.url)
            self.execute_stmt(sql, val)
            return
        try:

            shop_id = response.url.split('/')[4]
            if response.xpath('//span[@data-key="user_location"]//text()'):
                shop_location = response.xpath('//span[@data-key="user_location"]//text()').extract_first()

            if response.xpath("//span[contains(@class, 'etsy-since')]//text()"):
                shop_on_etsy_since = \
                    response.xpath("//span[contains(@class, 'etsy-since')]//text()").extract_first().split(' ')[3]

            if response.xpath('//a[@href="/shop/' + shop_id + '/sold"]//text()'):
                shop_sold = \
                    response.xpath('//a[@href="/shop/' + shop_id + '/sold"]//text()').extract_first().split(' ')[0]

            if response.xpath('//a[@href="/shop/' + shop_id + '/favoriters"]//text()'):
                shop_favorers = \
                    response.xpath('//a[@href="/shop/' + shop_id + '/favoriters"]//text()').extract_first().split(' ')[
                        0]

            if response.xpath('//input[@name="rating"]/@value'):
                shop_rating = response.xpath('//input[@name="rating"]/@value').extract_first()

            if response.xpath('//span[@data-inplace-editable-text="announcement"]//text()'):
                shop_anouncement = response.xpath(
                    '//span[@data-inplace-editable-text="announcement"]//text()').extract_first()

            if shop_sold == "0" and \
                    response.xpath("//div[contains(@class, 'shop-home-wider-sections')]/div[5]//text()").extract()[1]:
                shop_sold = \
                    response.xpath("//div[contains(@class, 'shop-home-wider-sections')]/div[5]//text()").extract()[
                        1].split(
                        ' ')[0]
            if response.xpath("//div[contains(@class, 'cover-photo-wrap')]/img/@src").extract_first():
                shop_cover_photo = response.xpath(
                    "//div[contains(@class, 'cover-photo-wrap')]/img/@src").extract_first()

            review_count = 0
            if response.xpath("//div[contains(@class, 'reviews-total')]/div/div/text()").extract():
                review_str = response.xpath("//div[contains(@class, 'reviews-total')]/div/div/text()").extract()[-1]
                if review_str == 'No reviews in the last year':
                    review_count = 0
                else:
                    review_count = review_str.replace("(","").replace(")", "")

            total_item_on_sale=0
            if response.xpath("//div[contains(@class, 'vertical-tabs')]/button/span/text()").extract():
                total_item_on_sale = response.xpath("//div[contains(@class, 'vertical-tabs')]/button/span/text()").extract()[1]

            items = "["
            if response.xpath("//div[contains(@class, 'vertical-tabs')]/button/span/text()").extract():
                i = 0
                while i < len(response.xpath("//div[contains(@class, 'vertical-tabs')]/button/span/text()").extract()):
                    item_type = response.xpath("//div[contains(@class, 'vertical-tabs')]/button/span/text()").extract()[i]
                    item_count = response.xpath("//div[contains(@class, 'vertical-tabs')]/button/span/text()").extract()[i+1]
                    i = i + 2
                    items = items + '{"type":"'+item_type + '", "count":"'+item_count+'"},'
            items = items + "]"

            is_sold_items_visible = 'N'

            if response.xpath("//a[contains(@href, 'sold')]//text()"):
                is_sold_items_visible = 'Y'


            location_chunks = shop_location.split(',')
            loc = country = ""
            if len(location_chunks) > 1:
                loc = location_chunks[0]
                country = location_chunks[1]
            else:
                loc = shop_location


            now = datetime.datetime.utcnow()

            sql = "insert into shop(shop_id, sold_count, favourer_count, review_count, rating, anouncement, cover_photo_1_url, " \
                  "crawl_date, location, country, year_found, total_item_on_sale, listed_items_by_type, is_sold_items_visible)" \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (shop_id, shop_sold, shop_favorers, review_count, shop_rating, shop_anouncement.encode('unicode_escape')[:3071],
                   shop_cover_photo, now.strftime('%Y-%m-%d %H:%M:%S'),loc, country, shop_on_etsy_since, total_item_on_sale, items, is_sold_items_visible)
            self.execute_stmt_no_commit(sql, val)

            sql = "update urls set status = %s, crawl_time=%s where url = %s"
            val = ('COMPLETED', now.strftime('%Y-%m-%d %H:%M:%S'), response.url)
            self.execute_stmt_no_commit(sql, val)
            self.my_db_connection.commit()

        except Exception as e:
            now = datetime.datetime.utcnow()
            sql = "update urls set status = %s, crawl_time=%s, crawl_detail=%s where url = %s"
            val = ('ERROR', now.strftime('%Y-%m-%d %H:%M:%S'),str(e), response.url)
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


    def execute_stmt_no_commit(self, stmt: str, vals):
        mycursor = self.my_db_connection.cursor()
        mycursor.execute(stmt, vals)
        return mycursor.lastrowid


    def get_all_rows(self, stmt: str, vals):
        mycursor = self.my_db_connection.cursor()
        mycursor.execute(stmt, vals)
        return mycursor.fetchall()
