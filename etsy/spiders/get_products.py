import datetime

import mysql.connector
import scrapy


# Spider Class
class GetProductsSpider(scrapy.Spider):
    # Spider name
    name = 'get_products'
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
        urls = []
        sql = "select url from category "
        val = ()
        ret = self.get_all_rows(sql, val)
        for r in ret:
            urls.append(r[0])

        self.start_urls = urls
        super(GetProductsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        response_url = response.url

        if response.url.find("page=") == -1:
            current_page_number = 1
            response_url = response_url + "?page=1#items"
        else:
            current_page_number = int(response.url.split('=')[-1])

        products_list = response.xpath('//a[contains(@class, "listing-link")]')

        categories = response.url[response_url.find("/c/") + 3:response_url.find("ref=pagination") - 1]

        for product in products_list:
            best_seller = ""
            if product.xpath('.//span[contains(@class, "wt-badge--status-03")]'):
                best_seller = product.xpath(
                    './/span[contains(@class, "wt-badge--status-03")]/span[2]//text()').extract_first()
            is_best_seller = 'N'
            if best_seller is not None:
                best_seller = best_seller.strip("\n \t")
                if best_seller == "Bestseller":
                    is_best_seller = 'Y'

            if is_best_seller == 'Y':
                product_title = product.xpath("./@title").extract_first()
                product_url = product.xpath("./@href").extract_first()
                listing_id = product.xpath("./@data-listing-id").extract_first()
                shop_name = product.xpath('.//div[contains(@class, "v2-listing-card__shop")]/p/text()').extract_first()

                sales_price = float(
                    product.xpath('.//span[contains(@class, "currency-value")]//text()').extract_first().replace(",",
                                                                                                                 ""))
                sales_currency = product.xpath('.//span[contains(@class, "currency-symbol")]//text()').extract_first()

                promotion_price = 0
                promotion_currency = ""

                priceList = product.xpath('.//span[contains(@class, "currency-value")]')
                if len(priceList) > 1:
                    promotion_price = float(priceList[1].xpath('.//text()').extract_first().replace(",", ""))

                discount_percentage = 0
                if promotion_price > 0:
                    promotion_currency = sales_currency
                    discount_percentage = 100 * float(sales_price) / promotion_price

                if discount_percentage > 0:
                    discount_percentage = 100 - int(discount_percentage)

                free_shipping = ""
                if product.xpath('.//span[contains(@class, "wt-badge--sale-01")]//text()'):
                    free_shipping = product.xpath(
                        './/span[contains(@class, "wt-badge--sale-01")]//text()').extract_first()
                free_shipping = free_shipping.strip("\n \t")



               # print("### shop : " + shop_name + " - " + listing_id + " - product title : " + product_title)
               # print("best_seller : " + best_seller + " - free_shipping : " + free_shipping)
               # print("https://etsy.com/listing/" + listing_id)
               # print("-------------")
                url = "https://etsy.com/listing/" + listing_id

                now = datetime.datetime.utcnow()
                is_free_shipping = 'N'
                if free_shipping == "FREE_SHIPPING":
                    is_free_shipping = 'Y'


                shop_review_count = 0
                shop_rating = 0
                if product.xpath('.//input[contains(@name, "rating")]/@value'):
                    shop_rating =  product.xpath('.//input[contains(@name, "rating")]/@value').extract_first()

                if product.xpath('.//span[contains(@class, "v2-listing-card__rating")]/span/text()'):
                    shop_review_count_str = product.xpath('.//span[contains(@class, "v2-listing-card__rating")]/span/text()').extract()[-1]
                    chunks = shop_review_count_str.split(" ")
                    if len(chunks) == 2:
                        shop_review_count = int(shop_review_count_str.split(" ")[0].replace(",",""))

                sql = "INSERT INTO  product ( LISTING_ID,TITLE,URL,IS_FREE_SHIPPING,IS_BEST_SELLER,SALES_PRICE,PROMO_PRICE, CURRENCY, DISCOUNT_PERCENTAGE," \
                      "SHOP_ID,SHOP_REVIEW_COUNT, SHOP_RATING, CATEGORY_URL,IS_ACTIVE, CRAWL_DATE)" \
                      "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )"
                val = (listing_id, product_title, url, is_free_shipping, is_best_seller, sales_price,
                       promotion_price, sales_currency, discount_percentage, shop_name, shop_review_count, shop_rating, response_url,  "Y",
                       now.strftime('%Y-%m-%d %H:%M:%S'))
                self.execute_stmt(sql, val)
            #print("# " + url)
            #yield scrapy.Request(url, callback=self.parse_product)

        if len(products_list)>0 :
            next_page_number = current_page_number + 1
            next_page_url = response_url[:response_url.find("page=") + 5] + str(next_page_number)

            yield response.follow(next_page_url, self.parse)


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


    def get_all_rows(self, stmt: str, vals):
        mycursor = self.my_db_connection.cursor()
        mycursor.execute(stmt, vals)
        return mycursor.fetchall()
