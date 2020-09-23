-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: finance_db
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alarm_info`
--

DROP TABLE IF EXISTS `alarm_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `alarm_info` (
  `client_id` varchar(255) NOT NULL COMMENT '사용자 파이어베이스 토큰',
  `alarm_data` varchar(255) DEFAULT NULL COMMENT '사용자가 가진 배당주 정보 및 알람 받고 싶은 정보',
  `volume` double DEFAULT NULL,
  `have_dividends` int(11) DEFAULT NULL COMMENT '0 이면 관심주, 1이면 보유주'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm_info`
--

LOCK TABLES `alarm_info` WRITE;
/*!40000 ALTER TABLE `alarm_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `alarm_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_info`
--

DROP TABLE IF EXISTS `client_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `client_info` (
  `firebase_token` varchar(255) NOT NULL,
  `alarm` int(11) NOT NULL DEFAULT '0' COMMENT '알림 받고 싶은 유무\n0 - 받고 싶지 않음\n1 - 받고 싶음',
  `client_id` varchar(45) NOT NULL,
  `have_dividends_alarm` int(11) DEFAULT NULL,
  `like_dividends_alarm` int(11) DEFAULT NULL,
  `have_payment_alarm` int(11) DEFAULT NULL,
  `like_payment_alarm` int(11) DEFAULT NULL,
  `monthly_alarm` int(11) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='고객 정보	';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_info`
--

LOCK TABLES `client_info` WRITE;
/*!40000 ALTER TABLE `client_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_rate_info`
--

DROP TABLE IF EXISTS `exchange_rate_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `exchange_rate_info` (
  `exchange_rate` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_rate_info`
--

LOCK TABLES `exchange_rate_info` WRITE;
/*!40000 ALTER TABLE `exchange_rate_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchange_rate_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_history_info`
--

DROP TABLE IF EXISTS `finance_history_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `finance_history_info` (
  `symbol` varchar(30) NOT NULL,
  `dividends_date` date DEFAULT NULL,
  `dividends` double DEFAULT NULL,
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`history_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_history_info`
--

LOCK TABLES `finance_history_info` WRITE;
/*!40000 ALTER TABLE `finance_history_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_history_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_info`
--

DROP TABLE IF EXISTS `finance_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `finance_info` (
  `symbol` varchar(30) NOT NULL COMMENT '상장회사 심벌',
  `name` varchar(100) DEFAULT NULL COMMENT '상장회사 이름',
  `dividends` double DEFAULT NULL COMMENT '배당금',
  `dividends_rate` double DEFAULT NULL COMMENT '배당금률',
  `dividends_date` date DEFAULT NULL COMMENT '배당락일',
  `payment_date` date DEFAULT NULL COMMENT '지급일',
  `hot_dividends` int(11) NOT NULL DEFAULT '0' COMMENT '배당주 리스트 포함 내용\\\\n0 - 킹, 귀족, 챔피언 속해있지 않음\\\\n1 - 킹\\\\n2 - 귀족\\\\n3 - 챔피언',
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_info`
--

LOCK TABLES `finance_info` WRITE;
/*!40000 ALTER TABLE `finance_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-23 17:48:34
