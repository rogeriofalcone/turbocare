-- MySQL dump 10.10
--
-- Host: localhost    Database: care2x
-- ------------------------------------------------------
-- Server version	5.1.12-beta

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
-- Table structure for table `care_users`
--

DROP TABLE IF EXISTS `care_users`;
CREATE TABLE `care_users` (
  `name` varchar(60) NOT NULL,
  `login_id` varchar(35) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `personell_nr` int(10) unsigned NOT NULL DEFAULT '0',
  `lockflag` tinyint(3) unsigned DEFAULT '0',
  `permission` text NOT NULL,
  `exc` tinyint(1) NOT NULL DEFAULT '0',
  `s_date` date NOT NULL DEFAULT '0000-00-00',
  `s_time` time NOT NULL DEFAULT '00:00:00',
  `expire_date` date NOT NULL DEFAULT '0000-00-00',
  `expire_time` time NOT NULL DEFAULT '00:00:00',
  `status` varchar(15) NOT NULL,
  `history` text NOT NULL,
  `modify_id` varchar(35) NOT NULL,
  `modify_time` datetime DEFAULT NULL,
  `create_id` varchar(35) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `login_id` (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `care_users`
--

LOCK TABLES `care_users` WRITE;
/*!40000 ALTER TABLE `care_users` DISABLE KEYS */;
INSERT INTO `care_users` VALUES ('Wesley','admin','202cb962ac59075b964b07152d234b70',0,0,'System_Admin',1,'0000-00-00','00:00:00','0000-00-00','00:00:00','','','admin','2006-05-27 15:06:49','admin','2006-11-24 11:12:17',1),('Another wes','wes','202cb962ac59075b964b07152d234b70',0,0,'',0,'0000-00-00','00:00:00','0000-00-00','00:00:00','','','',NULL,'','2006-11-24 11:12:17',5),('Inventory User','inv','202cb962ac59075b964b07152d234b70',0,0,'',0,'0000-00-00','00:00:00','0000-00-00','00:00:00','','','',NULL,'','2006-12-20 06:15:00',12),('Pharmacy User','phar','202cb962ac59075b964b07152d234b70',0,0,'',0,'0000-00-00','00:00:00','0000-00-00','00:00:00','','','',NULL,'','2006-12-20 06:15:00',10),('Registration User','reg','202cb962ac59075b964b07152d234b70',0,0,'',0,'0000-00-00','00:00:00','0000-00-00','00:00:00','','','',NULL,'','2006-12-20 06:15:00',11);
/*!40000 ALTER TABLE `care_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tg_group`
--

DROP TABLE IF EXISTS `tg_group`;
CREATE TABLE `tg_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(35) NOT NULL,
  `display_name` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_name` (`group_name`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tg_group`
--

LOCK TABLES `tg_group` WRITE;
/*!40000 ALTER TABLE `tg_group` DISABLE KEYS */;
INSERT INTO `tg_group` VALUES (1,'admin','Administrators','2006-05-29 16:31:00'),(2,'registration','Registration','2006-11-09 10:56:00'),(3,'inventory','Inventory','2006-11-09 10:56:00'),(7,'pharmacy_main','Pharmacy','2006-12-20 18:39:00'),(5,'warehouse main','Warehouse Main','2006-11-09 10:56:00'),(6,'billing','Billing','2006-12-19 08:50:00'),(8,'superuser','Super User','2006-12-21 10:24:00');
/*!40000 ALTER TABLE `tg_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tg_permissions`
--

DROP TABLE IF EXISTS `tg_permissions`;
CREATE TABLE `tg_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_name` varchar(35) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `permission_name` (`permission_name`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tg_permissions`
--

LOCK TABLES `tg_permissions` WRITE;
/*!40000 ALTER TABLE `tg_permissions` DISABLE KEYS */;
INSERT INTO `tg_permissions` VALUES (9,'bill_create','Create Bill'),(10,'bill_edit','Edit Bill'),(11,'bill_pay','Pay Bills'),(12,'bill_view','View Bills'),(15,'bill_delete','Bill Delete'),(16,'billing_report','Report Billing'),(17,'pharmacy_main_view','View Pharmacy Main'),(18,'warehouse_main_view','View Main Warehouse'),(19,'dispensing_view','Dispensing View'),(20,'dispensing_dispense','Dispensing'),(21,'reg_view','Registration View'),(22,'reg_create','Registration Create'),(23,'reg_edit','Reg Edit'),(24,'stores_catalog_view','Stores Catalog View '),(25,'stores_catalog_edit','Stores Catalog Edit'),(26,'stores_gr_view','Goods Received View'),(27,'stores_gr_edit','Goods Received Edit'),(28,'stores_quote_view','Stores Quote View'),(29,'stores_quote_edit','Stores Quote Editor'),(30,'stores_quoterequest_view','Quote Request View'),(33,'stores_vendor_view','Stores Vendor View'),(32,'stores_quoterequest_edit','Quote Request Edit'),(34,'stores_vendor_edit','Stores Vendor Edit'),(35,'stores_stock_view','Stock View'),(36,'stores_stock_edit','Stock Edit'),(37,'stores_stocktransferrequest_view','Stock Transfer Request View'),(38,'stores_stocktransferrequest_edit','Stock Transfer Request Edit'),(39,'stores_stocktransfer_view','Stock Transfer View'),(40,'stores_stocktransfer_edit','Stock Transfer Edit'),(41,'pharmacy_store_view','Pharmacy Store View'),(42,'warehouse_store_view','Warehouse Store View');
/*!40000 ALTER TABLE `tg_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2006-12-21 11:54:13
