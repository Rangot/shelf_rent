-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: shelf_rent
-- ------------------------------------------------------
-- Server version	5.5.46-log

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
-- Table structure for table `act`
--

DROP TABLE IF EXISTS `act`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `act` (
  `act_number` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `stop_date` date NOT NULL,
  `term` bigint(20) DEFAULT NULL,
  `payment` varchar(45) NOT NULL,
  `rents` int(11) DEFAULT NULL,
  `shelf` int(11) DEFAULT NULL,
  `timestamp` date NOT NULL,
  `updated` date NOT NULL,
  `term_left` bigint(20) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `all_payment` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`act_number`),
  UNIQUE KEY `act_shelf_051b0a75_uniq` (`shelf`),
  KEY `act_rents_4c9b24b7_fk_rents_rents_id` (`rents`),
  CONSTRAINT `act_rents_4c9b24b7_fk_rents_rents_id` FOREIGN KEY (`rents`) REFERENCES `rents` (`rents_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `act`
--

LOCK TABLES `act` WRITE;
/*!40000 ALTER TABLE `act` DISABLE KEYS */;
/*!40000 ALTER TABLE `act` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add act',7,'add_act'),(20,'Can change act',7,'change_act'),(21,'Can delete act',7,'delete_act'),(22,'Can add cash',8,'add_cash'),(23,'Can change cash',8,'change_cash'),(24,'Can delete cash',8,'delete_cash'),(25,'Can add orders',9,'add_orders'),(26,'Can change orders',9,'change_orders'),(27,'Can delete orders',9,'delete_orders'),(28,'Can add rents',10,'add_rents'),(29,'Can change rents',10,'change_rents'),(30,'Can delete rents',10,'delete_rents'),(31,'Can add shelf',11,'add_shelf'),(32,'Can change shelf',11,'change_shelf'),(33,'Can delete shelf',11,'delete_shelf'),(34,'Can add tenants',12,'add_tenants'),(35,'Can change tenants',12,'change_tenants'),(36,'Can delete tenants',12,'delete_tenants'),(37,'Can view log entry',1,'view_logentry'),(38,'Can view permission',2,'view_permission'),(39,'Can view group',3,'view_group'),(40,'Can view user',4,'view_user'),(41,'Can view content type',5,'view_contenttype'),(42,'Can view session',6,'view_session'),(43,'Can view act',7,'view_act'),(44,'Can view cash',8,'view_cash'),(45,'Can view Order',9,'view_orders'),(46,'Can view Rent',10,'view_rents'),(47,'Can view shelf',11,'view_shelf'),(48,'Can view Tenant',12,'view_tenants');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$hSMmiLLJe5dB$h/hxkTeVUaIkE023DGu8r6bse2SEeaJmpvT8uqmsCBE=','2018-09-20 11:30:59',1,'admin','','','',1,1,'2018-07-11 19:46:03');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cash`
--

DROP TABLE IF EXISTS `cash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cash` (
  `id_cash` int(11) NOT NULL AUTO_INCREMENT,
  `cash_date` datetime NOT NULL,
  `sell` varchar(45) NOT NULL,
  `take` varchar(45) NOT NULL,
  `discount` varchar(45) DEFAULT NULL,
  `orders` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_cash`),
  KEY `cash_orders_52fb5be9_fk_orders_orders_id` (`orders`),
  CONSTRAINT `cash_orders_52fb5be9_fk_orders_orders_id` FOREIGN KEY (`orders`) REFERENCES `orders` (`orders_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cash`
--

LOCK TABLES `cash` WRITE;
/*!40000 ALTER TABLE `cash` DISABLE KEYS */;
/*!40000 ALTER TABLE `cash` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-08-07 21:11:23','5','Tenants object (5)',3,'',12,1),(2,'2018-08-07 21:11:23','4','Tenants object (4)',3,'',12,1),(3,'2018-08-07 21:11:23','3','Tenants object (3)',3,'',12,1),(4,'2018-08-07 21:11:23','2','Tenants object (2)',3,'',12,1),(5,'2018-08-08 18:15:02','1','Shelf object (1)',1,'[{\"added\": {}}]',11,1),(6,'2018-08-08 18:15:32','2','Shelf object (2)',1,'[{\"added\": {}}]',11,1),(7,'2018-08-08 18:27:04','1','Rents object (1)',1,'[{\"added\": {}}]',10,1),(8,'2018-08-08 18:28:17','2','Rents object (2)',1,'[{\"added\": {}}]',10,1),(9,'2018-08-08 18:40:22','1','Act object (1)',1,'[{\"added\": {}}]',7,1),(10,'2018-08-08 18:47:20','2','Act object (2)',1,'[{\"added\": {}}]',7,1),(11,'2018-08-08 18:49:52','1','Act object (1)',3,'',7,1),(12,'2018-08-08 18:50:26','2','Act object (2)',3,'',7,1),(13,'2018-08-08 18:54:30','1','Act object (1)',1,'[{\"added\": {}}]',7,1),(14,'2018-08-08 18:55:20','1','Act object (1)',2,'[{\"changed\": {\"fields\": [\"stop_date\"]}}]',7,1),(15,'2018-08-08 18:55:56','2','Act object (2)',1,'[{\"added\": {}}]',7,1),(16,'2018-08-08 19:35:45','3','Act object (3)',1,'[{\"added\": {}}]',7,1),(17,'2018-08-08 19:39:24','3','Act object (3)',2,'[]',7,1),(18,'2018-08-09 13:15:04','3','Act object (3)',1,'[{\"added\": {}}]',7,1),(19,'2018-08-09 13:19:21','3','Act object (3)',2,'[{\"changed\": {\"fields\": [\"payment\"]}}]',7,1),(20,'2018-08-09 13:20:17','3','Act object (3)',2,'[{\"changed\": {\"fields\": [\"stop_date\"]}}]',7,1),(21,'2018-08-09 13:24:20','3','Act object (3)',2,'[]',7,1),(22,'2018-08-09 19:17:15','3','Act object (3)',2,'[{\"changed\": {\"fields\": [\"rents\", \"shelf\"]}}]',7,1),(23,'2018-08-09 19:35:55','2','Батиков Роман Игоревич',2,'[{\"changed\": {\"fields\": [\"stop_date\"]}}]',10,1),(24,'2018-08-09 19:54:29','3','Батиков Роман Игоревич',1,'[{\"added\": {}}]',10,1),(25,'2018-08-09 20:01:31','4','Батиков Роман Игоревич',1,'[{\"added\": {}}]',10,1),(26,'2018-08-09 20:02:01','5','Батиков Роман Игоревич',1,'[{\"added\": {}}]',10,1),(27,'2018-08-12 17:31:30','7','Иванов Сергей Борисович',1,'[{\"added\": {}}]',10,1),(28,'2018-08-21 19:36:43','7','Батиков Роман Игоревич',2,'[{\"changed\": {\"fields\": [\"email\"]}}]',12,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'tenants_app','act'),(8,'tenants_app','cash'),(9,'tenants_app','orders'),(10,'tenants_app','rents'),(11,'tenants_app','shelf'),(12,'tenants_app','tenants');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-06-29 19:05:06'),(2,'auth','0001_initial','2018-06-29 19:05:07'),(3,'admin','0001_initial','2018-06-29 19:05:07'),(4,'admin','0002_logentry_remove_auto_add','2018-06-29 19:05:07'),(5,'contenttypes','0002_remove_content_type_name','2018-06-29 19:05:07'),(6,'auth','0002_alter_permission_name_max_length','2018-06-29 19:05:07'),(7,'auth','0003_alter_user_email_max_length','2018-06-29 19:05:08'),(8,'auth','0004_alter_user_username_opts','2018-06-29 19:05:08'),(9,'auth','0005_alter_user_last_login_null','2018-06-29 19:05:08'),(10,'auth','0006_require_contenttypes_0002','2018-06-29 19:05:08'),(11,'auth','0007_alter_validators_add_error_messages','2018-06-29 19:05:08'),(12,'auth','0008_alter_user_username_max_length','2018-06-29 19:05:08'),(13,'auth','0009_alter_user_last_name_max_length','2018-06-29 19:05:08'),(14,'sessions','0001_initial','2018-06-29 19:05:08'),(15,'tenants_app','0001_initial','2018-06-29 19:05:09'),(16,'tenants_app','0002_auto_20180711_2334','2018-07-11 20:34:49'),(17,'tenants_app','0003_auto_20180807_2344','2018-08-07 20:44:40'),(18,'tenants_app','0004_auto_20180808_0001','2018-08-07 21:02:04'),(19,'tenants_app','0005_auto_20180808_0008','2018-08-07 21:09:05'),(20,'tenants_app','0006_auto_20180808_2146','2018-08-08 18:46:19'),(21,'tenants_app','0007_auto_20180808_2153','2018-08-08 18:53:41'),(22,'tenants_app','0008_auto_20180808_2234','2018-08-08 19:34:42'),(23,'tenants_app','0009_auto_20180808_2255','2018-08-08 19:55:07'),(24,'tenants_app','0010_act_is_active','2018-08-09 12:03:10'),(25,'tenants_app','0011_auto_20180809_1516','2018-08-09 12:16:10'),(26,'tenants_app','0012_auto_20180809_1537','2018-08-09 12:39:01'),(27,'tenants_app','0011_auto_20180809_1552','2018-08-09 12:52:09'),(28,'tenants_app','0011_auto_20180809_1555','2018-08-09 12:55:07'),(29,'tenants_app','0012_auto_20180809_1600','2018-08-09 13:00:51'),(30,'tenants_app','0013_auto_20180809_1609','2018-08-09 13:10:00'),(31,'tenants_app','0014_auto_20180809_1614','2018-08-09 13:14:22'),(32,'tenants_app','0015_auto_20180809_2228','2018-08-09 19:28:36'),(33,'tenants_app','0016_auto_20180809_2235','2018-08-09 19:35:12'),(34,'tenants_app','0017_auto_20180811_0051','2018-08-10 21:52:03'),(35,'tenants_app','0018_auto_20180815_1515','2018-08-15 12:15:20'),(36,'tenants_app','0019_auto_20180815_2119','2018-08-15 18:19:17'),(37,'tenants_app','0020_auto_20180815_2120','2018-08-15 18:21:03'),(38,'tenants_app','0021_auto_20180816_1624','2018-08-16 13:24:47'),(39,'tenants_app','0022_auto_20180822_1310','2018-08-22 10:10:34'),(40,'tenants_app','0023_auto_20180822_1409','2018-08-22 11:10:08'),(41,'tenants_app','0024_auto_20180822_1420','2018-08-22 11:20:50'),(42,'tenants_app','0025_auto_20180822_1509','2018-08-22 12:10:05'),(43,'tenants_app','0026_auto_20180822_2105','2018-08-22 18:05:25'),(44,'tenants_app','0027_auto_20180823_0016','2018-08-22 21:17:53'),(45,'tenants_app','0028_auto_20180823_1454','2018-08-23 11:54:44'),(46,'tenants_app','0029_auto_20180823_2243','2018-08-23 19:43:33'),(47,'tenants_app','0030_auto_20180823_2253','2018-08-23 19:53:45'),(48,'tenants_app','0031_auto_20180823_2258','2018-08-23 19:58:19'),(49,'tenants_app','0032_auto_20180827_0054','2018-08-26 21:54:13'),(50,'tenants_app','0033_auto_20180829_1543','2018-08-29 12:43:54'),(51,'tenants_app','0034_auto_20180829_1655','2018-08-29 13:56:04'),(52,'tenants_app','0035_auto_20180829_1703','2018-08-29 14:03:21'),(53,'tenants_app','0036_auto_20180905_1647','2018-09-05 13:47:23'),(54,'admin','0003_logentry_add_action_flag_choices','2018-09-06 10:10:39'),(55,'tenants_app','0037_auto_20180920_1442','2018-09-20 11:42:42'),(56,'tenants_app','0038_auto_20180920_1500','2018-09-20 12:00:49'),(57,'tenants_app','0039_auto_20180920_1511','2018-09-20 12:11:27'),(58,'tenants_app','0040_auto_20180920_1516','2018-09-20 12:17:00'),(59,'tenants_app','0041_auto_20180920_1519','2018-09-20 12:19:54');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('62sl9xokn6cne0709346z9y7w546le05','Y2Q0Mjc4MWJiZjU0YjA1NTdmNDU5ZDAzZDBkYTgzZmM2NTBmYjJmODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNDE5NjY1MjNhZTAyMWQ3ODEzOTU3Mjg0N2JjMzlhZWJhNGI0ZmExIn0=','2018-09-20 10:11:10'),('7zzq3cvoiu4219d5hsg2hrn8o2u72975','YTA5ZmQ4ZjY1YzIyOWUxNDdjMDMxZDE4Y2FhNDZlM2QwZjljY2FiMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZmY2MDU2MTY2OWFhMjMzMmI0NTlkMmU0NTM4NTkyNmYwOTgyMjRhIn0=','2018-07-27 19:52:14'),('cawdtjg00hoh8tzw702lbqcwu5ty938i','YTA5ZmQ4ZjY1YzIyOWUxNDdjMDMxZDE4Y2FhNDZlM2QwZjljY2FiMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZmY2MDU2MTY2OWFhMjMzMmI0NTlkMmU0NTM4NTkyNmYwOTgyMjRhIn0=','2018-09-04 19:36:16'),('eyhxmqanaqoc9ho8sx1vvfz59j2o7qkh','Y2Q0Mjc4MWJiZjU0YjA1NTdmNDU5ZDAzZDBkYTgzZmM2NTBmYjJmODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNDE5NjY1MjNhZTAyMWQ3ODEzOTU3Mjg0N2JjMzlhZWJhNGI0ZmExIn0=','2018-10-04 11:30:59'),('if7suwicivz2erxdkgwo1wca0vafe2br','YTA5ZmQ4ZjY1YzIyOWUxNDdjMDMxZDE4Y2FhNDZlM2QwZjljY2FiMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZmY2MDU2MTY2OWFhMjMzMmI0NTlkMmU0NTM4NTkyNmYwOTgyMjRhIn0=','2018-08-21 21:10:54'),('x8yvm2lwp0hzxmzxbf53coejq6vq5cac','YTA5ZmQ4ZjY1YzIyOWUxNDdjMDMxZDE4Y2FhNDZlM2QwZjljY2FiMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZmY2MDU2MTY2OWFhMjMzMmI0NTlkMmU0NTM4NTkyNmYwOTgyMjRhIn0=','2018-07-25 19:46:36');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `orders_id` int(11) NOT NULL AUTO_INCREMENT,
  `name_item` varchar(45) DEFAULT NULL,
  `description_item` varchar(100) DEFAULT NULL,
  `quality` varchar(45) NOT NULL,
  `price` varchar(45) DEFAULT NULL,
  `act` int(11) NOT NULL,
  `materials` varchar(45) DEFAULT NULL,
  `all_sell` varchar(45) NOT NULL,
  `all_take` varchar(45) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`orders_id`),
  KEY `orders_act_7df5dfcd` (`act`),
  CONSTRAINT `orders_act_7df5dfcd_fk_act_act_number` FOREIGN KEY (`act`) REFERENCES `act` (`act_number`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rents`
--

DROP TABLE IF EXISTS `rents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rents` (
  `rents_id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(45) DEFAULT NULL,
  `start_date` date NOT NULL,
  `stop_date` date NOT NULL,
  `tenants` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `term_left` bigint(20) DEFAULT NULL,
  `updated` date NOT NULL,
  PRIMARY KEY (`rents_id`),
  UNIQUE KEY `rents_number_2b5ca72c_uniq` (`number`),
  KEY `rents_tenants_01292df7_fk_tenants_tenants_id` (`tenants`),
  CONSTRAINT `rents_tenants_01292df7_fk_tenants_tenants_id` FOREIGN KEY (`tenants`) REFERENCES `tenants` (`tenants_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rents`
--

LOCK TABLES `rents` WRITE;
/*!40000 ALTER TABLE `rents` DISABLE KEYS */;
/*!40000 ALTER TABLE `rents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelf`
--

DROP TABLE IF EXISTS `shelf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shelf` (
  `shelf_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `price` int(11) DEFAULT NULL,
  PRIMARY KEY (`shelf_id`),
  UNIQUE KEY `shelf_name_515c4b5e_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelf`
--

LOCK TABLES `shelf` WRITE;
/*!40000 ALTER TABLE `shelf` DISABLE KEYS */;
/*!40000 ALTER TABLE `shelf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenants`
--

DROP TABLE IF EXISTS `tenants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenants` (
  `tenants_id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `pass_given` longtext,
  `pass_number` varchar(6) DEFAULT NULL,
  `pass_serial` varchar(4) DEFAULT NULL,
  `telephone` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tenants_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenants`
--

LOCK TABLES `tenants` WRITE;
/*!40000 ALTER TABLE `tenants` DISABLE KEYS */;
/*!40000 ALTER TABLE `tenants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-21 23:16:11
