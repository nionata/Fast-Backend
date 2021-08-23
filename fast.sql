-- -------------------------------------------------------------
-- TablePlus 3.12.5(364)
--
-- https://tableplus.com/
--
-- Database: fast
-- Generation Time: 2021-08-22 23:25:30.2920
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `attendance_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `attendance_event_id` bigint unsigned NOT NULL,
  `attendance_member_id` bigint unsigned NOT NULL,
  `attendance_time_in` bigint unsigned NOT NULL,
  PRIMARY KEY (`attendance_id`),
  UNIQUE KEY `id` (`attendance_id`),
  KEY `event_id` (`attendance_event_id`),
  KEY `member_id` (`attendance_member_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`attendance_event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`attendance_member_id`) REFERENCES `members` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `event_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `event_name` text NOT NULL,
  `event_start` int NOT NULL,
  `event_end` bigint unsigned NOT NULL,
  `event_lat` float NOT NULL,
  `event_long` float NOT NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `id` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `members`;
CREATE TABLE `members` (
  `member_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `member_first_name` text NOT NULL,
  `member_last_name` text NOT NULL,
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `id` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;