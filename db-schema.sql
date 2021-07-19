/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `item_count` int(11) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=162 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `LISTING_ID` int(11) NOT NULL,
  `TITLE` varchar(255) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `IS_FREE_SHIPPING` varchar(255) DEFAULT NULL,
  `IS_BEST_SELLER` varchar(255) DEFAULT NULL,
  `SALES_PRICE` double DEFAULT NULL,
  `PROMO_PRICE` double DEFAULT NULL,
  `CURRENCY` varchar(255) DEFAULT NULL,
  `DISCOUNT_PERCENTAGE` double DEFAULT NULL,
  `SHOP_ID` varchar(255) DEFAULT NULL,
  `SHOP_REVIEW_COUNT` int(11) DEFAULT NULL,
  `SHOP_RATING` double DEFAULT NULL,
  `CATEGORY_URL` varchar(255) DEFAULT NULL,
  `IS_ACTIVE` varchar(255) DEFAULT NULL,
  `CRAWL_DATE` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop`
--

DROP TABLE IF EXISTS `shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop` (
  `shop_id` varchar(255) NOT NULL,
  `sold_count` int(11) DEFAULT NULL,
  `favourer_count` int(11) DEFAULT NULL,
  `review_count` int(11) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `anouncement` text,
  `cover_photo_1_url` varchar(255) DEFAULT NULL,
  `crawl_date` datetime DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `year_found` varchar(45) DEFAULT NULL,
  `total_item_on_sale` int(11) DEFAULT NULL,
  `listed_items_by_type` text,
  `is_sold_items_visible` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`shop_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `urls`
--

DROP TABLE IF EXISTS `urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `urls` (
  `url` varchar(255) NOT NULL,
  `item_type` varchar(255) DEFAULT NULL,
  `url_type` varchar(45) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `item_count` int(11) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL,
  `crawl_detail` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

