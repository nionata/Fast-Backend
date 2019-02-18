-- MySQL dump 10.13  Distrib 8.0.13, for macos10.14 (x86_64)
--
-- Host: localhost    Database: fast
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `attendance` (
  `attendance_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `attendance_event_id` bigint(20) DEFAULT NULL,
  `attendance_member_id` bigint(20) DEFAULT NULL,
  `attendance_time_in` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`attendance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (44,41,58,1549383842),(45,42,58,1549384975),(46,42,59,1549385143),(47,43,58,1549515384),(48,43,55,1549515971),(49,44,58,1549516071);
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `events` (
  `event_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `event_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_type_id` bigint(20) DEFAULT NULL,
  `event_start` bigint(20) DEFAULT NULL,
  `event_end` bigint(20) DEFAULT NULL,
  `event_lat` decimal(10,8) DEFAULT NULL,
  `event_long` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (35,'Test',1,1549249195,1647441932,29.65308000,-82.33996000),(36,'66',1,1549252301,1549255601,29.65309870,-82.33996310),(37,'Chapter',1,1549252797,1549254597,29.65306860,-82.33994200),(38,'Chapter',1,1549252797,1549254597,29.65306860,-82.33994200),(39,'123',1,1549254511,1549254571,29.65309710,-82.33993960),(40,'Ligma',1,1549381817,1647441932,29.65308000,-82.33996000),(41,'Hi MOm',1,1549383835,1647441932,29.65308000,-82.33996000),(42,'Zack',1,1549384917,1647441932,29.65308000,-82.33996000),(43,'Michael\'s Birthday',1,1549515311,1647441932,29.65308000,-82.33996000),(44,'Chapter',1,1549516063,1647441932,29.65308000,-82.33996000);
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `members` (
  `member_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `member_first_name` varchar(45) DEFAULT NULL,
  `member_last_name` varchar(45) DEFAULT NULL,
  `member_points` bigint(20) DEFAULT '0',
  PRIMARY KEY (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (4,'Palmer','Alvarez',0),(5,'Eric','AmRhein',0),(6,'Sebastian','Angeli',0),(7,'Austin','Barton',0),(8,'Gray','Bean',0),(9,'Walker ','Bean',0),(10,'Kyle','Bechakas',0),(11,'Ryan','Belfiore',0),(12,'Roberto','Bettaglio',0),(13,'Sam','Bishop',0),(14,'Bobby','Brunner',0),(15,'Robert','Bruns',0),(16,'Nick','Bryant',0),(17,'Ethan','Budowsky',0),(18,'Justin','Burt',0),(19,'Jason','Caldwell',0),(20,'Nick','Callaway',0),(21,'Alex','Caputo',0),(22,'Austin','Carroll',0),(23,'Jack','Clark',0),(24,'Trent','Cole',0),(25,'Joseph','Cucci',0),(26,'Davis ','Curry',0),(27,'Nick','Decker',0),(28,'Nick','Denfeld',0),(29,'Dwyer','Dominguez',0),(30,'Jack','Drohan',0),(31,'Garritt','Dubois',0),(32,'Andrew ','Early',0),(33,'Connor','Elkin',0),(34,'Sam','Ellis',0),(35,'Tony','Emmett',0),(36,'Josh','Evans',0),(37,'Scotty','Exum',0),(38,'Nathan','Friedman',0),(39,'Adam','Frisco',0),(40,'Wolfgang','Fry-Eastin',0),(41,'Joey','Galbraith',0),(42,'Matthew','Galluzzo',0),(43,'Chris','Garbo',0),(44,'Adler','Garfield',0),(45,'Kyle','Gauger',0),(46,'Logan','Golladay',0),(47,'Jared','Grigas',0),(48,'Ryan','Hagan',0),(49,'Chris','Harris',0),(50,'John','Hench',0),(51,'Andres','Henriquez',0),(52,'Jack','Hertz',0),(53,'Jake','Hill',0),(54,'Ryan','Hinterleiter',0),(55,'Dirk','Hoening',0),(56,'Grant','Husted',0),(57,'Tommy','Hutchinson',0),(58,'Nick','Ionata',0),(59,'Matthew','Ionescu',0),(60,'Sajid','Jafferjee',0),(61,'Nick','Jagodzinski',0),(62,'Pierce','Kimbrough',0),(63,'Cooper','Kirkland',0),(64,'Austin','Klein',0),(65,'Joseph','Lanese',0),(66,'Jt','Le',0),(67,'Daniel','Lively',0),(68,'Nathan','Lunsford',0),(69,'Zach','machado',0),(70,'Skyler','MaCleod',0),(71,'Joe','Mccoy',0),(72,'Aaron','Mills',0),(73,'Lucas','Mingote',0),(74,'Cameron','Mockabee',0),(75,'Ollie','Monaghan',0),(76,'Patrick','Morano',0),(77,'Zane','Mueller',0),(78,'Zac','Murphy',0),(79,'Connor','Neff',0),(80,'Drew','Nelson',0),(81,'Alex','Ngo',0),(82,'Gregory','Ohl',0),(83,'Harold','Pan',0),(84,'Curtis','Patillo',0),(85,'Kyle','Pollock',0),(86,'Patrick','Prieto',0),(87,'Manny','Ramirez',0),(88,'Austin','Ransdell',0),(89,'Chase','Reineke',0),(90,'Grant','Robinson',0),(91,'Shane','Rocklein',0),(92,'Devon','Rodriguez',0),(93,'Alex','Roetzheim',0),(94,'Shaun','Rogozinski',0),(95,'Marco','Romano',0),(96,'Christian','Ruiz',0),(97,'Miguel','Ruiz',0),(98,'Sam','Salinas',0),(99,'Jacob','Salminen',0),(100,'Shawn','Salo',0),(101,'Ali','Sammour',0),(102,'Will','Sandifer',0),(103,'Zach ','Schacter',0),(104,'Trevor','Schaettle',0),(105,'Brennan','Schmitz',0),(106,'James','Schnell',0),(107,'Braden','Schopke',0),(108,'Adam','Scott',0),(109,'Dylan','Shaw',0),(110,'James','Shea',0),(111,'Will','Shidler',0),(112,'Donny','Spillane',0),(113,'Ben ','Spivey',0),(114,'Evan','Stone',0),(115,'Curtis','Stump',0),(116,'Garett','Taylor',0),(117,'Cole','Tollett',0),(118,'Connor','Townsend',0),(119,'Cody','Tsai',0),(120,'Justin','Tunley',0),(121,'Serge','Melnik',0),(122,'Russell','Vaccaro',0),(123,'Alex','Varidin',0),(124,'Christopher','Walker',0),(125,'Jack','Walker',0),(126,'Tyler','Wallace',0),(127,'David','Weck',0),(128,'Cody','Wheeler',0);
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `types` (
  `type_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(45) DEFAULT NULL,
  `type_points` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `types`
--

LOCK TABLES `types` WRITE;
/*!40000 ALTER TABLE `types` DISABLE KEYS */;
INSERT INTO `types` VALUES (1,'chapter',10);
/*!40000 ALTER TABLE `types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-18 12:09:44
