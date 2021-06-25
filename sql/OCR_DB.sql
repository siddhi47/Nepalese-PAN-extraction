-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: OCR_DB
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ocr_ird_pan_details`
--

DROP TABLE IF EXISTS `ocr_ird_pan_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocr_ird_pan_details` (
  `id` int NOT NULL,
  `pan_no` bigint DEFAULT NULL,
  `name` varchar(225) DEFAULT NULL,
  `name_nepali` varchar(255) DEFAULT NULL,
  `business_name` varchar(225) DEFAULT NULL,
  `business_name_nepali` varchar(225) DEFAULT NULL,
  `telephone` bigint DEFAULT NULL,
  `street_name` varchar(255) DEFAULT NULL,
  `ward` tinyint DEFAULT NULL,
  `office` varchar(255) DEFAULT NULL,
  `registration_type` varchar(50) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT NULL,
  `created_by` varchar(10) DEFAULT NULL,
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(10) DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocr_ird_pan_details`
--

LOCK TABLES `ocr_ird_pan_details` WRITE;
/*!40000 ALTER TABLE `ocr_ird_pan_details` DISABLE KEYS */;
INSERT INTO `ocr_ird_pan_details` VALUES (0,606685254,'Extensodata Pvt. Ltd','एक्सटेनसोडाटा प्रा.लि.','Extensodata Pvt. Ltd','एक्सटेनसोडाटा प्रा.लि.',9801079616,'हात्तीसार',1,'आन्तरिक राजस्व कार्यालय पुतलीसडक','Income Tax','2075-03-21 00:00:00','active',NULL,'2021-02-09 12:07:51',NULL,NULL),(1,301906438,'F1soft Pvt. Ltd.','एफ १ सफ्ट ईन्टरनेशनल प्रा.लि.','F1soft Pvt. Ltd.','ठूला करदाता कार्यालय',4442435,'पुतलिसडक',1,'ठूला करदाता कार्यालय','Income Tax','2062-01-09 00:00:00','active',NULL,'2021-02-09 12:10:44',NULL,NULL),(2,607596970,'Chartered Global',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'active',NULL,'2021-02-23 15:31:24',NULL,NULL);
/*!40000 ALTER TABLE `ocr_ird_pan_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocr_pan_details`
--

DROP TABLE IF EXISTS `ocr_pan_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocr_pan_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pan_no` bigint DEFAULT NULL,
  `business_name` varchar(255) DEFAULT NULL,
  `business_type` varchar(225) DEFAULT NULL,
  `created_by` varchar(10) DEFAULT NULL,
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(10) DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocr_pan_details`
--

LOCK TABLES `ocr_pan_details` WRITE;
/*!40000 ALTER TABLE `ocr_pan_details` DISABLE KEYS */;
INSERT INTO `ocr_pan_details` VALUES (1,606685254,'Extensodata Pvt. Ltd','1',NULL,'2021-02-09 12:24:04',NULL,NULL),(2,301906438,'F1soft Pvt. Ltd.','1',NULL,'2021-02-09 12:24:04',NULL,NULL),(4,607596970,'Chartered Global','1',NULL,'2021-02-23 15:31:41',NULL,NULL);
/*!40000 ALTER TABLE `ocr_pan_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocr_pan_results`
--

DROP TABLE IF EXISTS `ocr_pan_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocr_pan_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_path` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pan_no` bigint DEFAULT NULL,
  `business_name_nepali` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `business_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `business_type_nepali` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `business_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image_resolution` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `remarks` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_by` varchar(25) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(25) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocr_pan_results`
--

LOCK TABLES `ocr_pan_results` WRITE;
/*!40000 ALTER TABLE `ocr_pan_results` DISABLE KEYS */;
INSERT INTO `ocr_pan_results` VALUES (1,'/app/test_image/Company PAN03.jpg',672354339,'मेन्टर प्रा. ’ ले.','mentar praa. ’ le. ','लिमिटेड','limited ','2284X1660',NULL,NULL,'2021-02-25 10:33:56',NULL,NULL),(2,'/app/test_image/Company PAN06.jpg',NULL,'चार्टर्ड ग्लोबल ह्युमन प्रा.लि.','chaartarda global hyuman praa.li. ','प्राइभैट','praaibhait ','3508X2499',NULL,NULL,'2021-02-25 10:33:56',NULL,NULL),(3,'/app/test_image/Company PAN07.jpeg',603304439,'माउन्टैन प्रा. लि.','maauntain praa. li. ','',' ','3340X2550',NULL,NULL,'2021-02-25 10:33:56',NULL,NULL);
/*!40000 ALTER TABLE `ocr_pan_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocr_verification`
--

DROP TABLE IF EXISTS `ocr_verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocr_verification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pan_result_id` int DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `is_ird_verified` tinyint(1) DEFAULT NULL,
  `is_internal_verified` tinyint(1) DEFAULT NULL,
  `is_pan_no_present` tinyint(1) DEFAULT NULL,
  `is_business_type_present` tinyint(1) DEFAULT NULL,
  `is_business_name_present` tinyint(1) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `created_by` varchar(20) DEFAULT NULL,
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(20) DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocr_verification`
--

LOCK TABLES `ocr_verification` WRITE;
/*!40000 ALTER TABLE `ocr_verification` DISABLE KEYS */;
/*!40000 ALTER TABLE `ocr_verification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-25 10:58:49
