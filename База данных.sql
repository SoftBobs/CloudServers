-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: cloudservers
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actionlogs`
--

DROP TABLE IF EXISTS `actionlogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actionlogs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  `vm_id` int NOT NULL,
  `action` varchar(255) NOT NULL,
  `date_time` datetime NOT NULL,
  `ip_address` varchar(255) NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `student_id` (`student_id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `vm_id` (`vm_id`),
  CONSTRAINT `actionlogs_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `actionlogs_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`),
  CONSTRAINT `actionlogs_ibfk_3` FOREIGN KEY (`vm_id`) REFERENCES `virtualmachines` (`vm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actionlogs`
--

LOCK TABLES `actionlogs` WRITE;
/*!40000 ALTER TABLE `actionlogs` DISABLE KEYS */;
INSERT INTO `actionlogs` VALUES (9,1,NULL,1,'Создание VM','2024-03-27 19:17:36','192.168.1.100'),(10,NULL,1,2,'Удаление VM','2024-03-27 19:17:36','192.168.1.101'),(11,2,NULL,3,'Обновление VM','2024-03-27 19:17:36','192.168.1.102'),(12,NULL,2,4,'Перезагрузка VM','2024-03-27 19:17:36','192.168.1.103');
/*!40000 ALTER TABLE `actionlogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authconfigs`
--

DROP TABLE IF EXISTS `authconfigs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authconfigs` (
  `config_id` int NOT NULL AUTO_INCREMENT,
  `auth_url` varchar(255) NOT NULL,
  `project_name` varchar(255) NOT NULL,
  `project_domain_name` varchar(255) NOT NULL,
  `user_domain_name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `auth_type` varchar(255) NOT NULL,
  PRIMARY KEY (`config_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authconfigs`
--

LOCK TABLES `authconfigs` WRITE;
/*!40000 ALTER TABLE `authconfigs` DISABLE KEYS */;
INSERT INTO `authconfigs` VALUES (1,'https://api.immers.cloud:5000/v3','IlyaUdalinin','default','default','IlyaUdalinin','Homersimpson51','v3password');
/*!40000 ALTER TABLE `authconfigs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configurations`
--

DROP TABLE IF EXISTS `configurations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configurations` (
  `configuration_id` int NOT NULL AUTO_INCREMENT,
  `configuration_name` varchar(255) NOT NULL,
  `openstack_id` varchar(255) NOT NULL,
  PRIMARY KEY (`configuration_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configurations`
--

LOCK TABLES `configurations` WRITE;
/*!40000 ALTER TABLE `configurations` DISABLE KEYS */;
INSERT INTO `configurations` VALUES (1,'teslat4-1.8.32.80','962ea4d2-24c3-4222-8118-16e887ec0539'),(2,'rtx4090-1.8.32.240','6e8094c1-eb39-4b8a-86b7-f816e880de10'),(3,'rtx4090-4.16.32.160','66347b3c-2feb-49ec-8884-3799304d59e0'),(4,'teslaa100-1.16.128.160','1a4f12d1-b686-42f8-8b01-18843bf42f11'),(5,'rtx3090-1.16.64.160','def27667-75f7-48f7-943f-e9ddb9bced96');
/*!40000 ALTER TABLE `configurations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `image_name` varchar(255) NOT NULL,
  `openstack_id` varchar(255) NOT NULL,
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (1,'Windows Server 2022 Standard','e82e90e6-42b2-49ef-8f73-17e6024d0a66'),(2,'Windows Server 2022 Standard Tesla Driver','1193ce33-c09d-4ae0-ac8c-7b47fe0111d6'),(3,'Ubuntu 22.04.4 CUDA 12.3','bed68aee-a09d-480e-9402-7a7d1e0a33d5'),(4,'Ubuntu 22.04 Jupyter Notebook','213f8e38-c2a6-4619-9224-8ccb1711ec16'),(5,'CentOS 8 (20.11)','b181fd38-37c2-4b84-985f-0ab2a6e057ea'),(6,'тест Ubuntu','4cbc3a3b-d5e9-4bd4-bd15-5e02c0610129'),(7,'тест Windows Server','5c00b2a5-6923-4bed-bbf4-25690120d80e');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `initializationscripts`
--

DROP TABLE IF EXISTS `initializationscripts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `initializationscripts` (
  `script_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `script_content` text NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`script_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `initializationscripts`
--

LOCK TABLES `initializationscripts` WRITE;
/*!40000 ALTER TABLE `initializationscripts` DISABLE KEYS */;
INSERT INTO `initializationscripts` VALUES (1,'Установка Nginx','apt-get update && apt-get install -y nginx','2024-03-27 19:11:26'),(2,'Установка Docker','curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh','2024-03-27 19:11:26'),(3,'Настройка среды Python','apt-get update && apt-get install -y python3-pip','2024-03-27 19:11:26'),(4,'Установка MySQL сервера','apt-get update && apt-get install -y mysql-server','2024-03-27 19:11:26');
/*!40000 ALTER TABLE `initializationscripts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Иван','Иванов','ivanivanov','Pass12345'),(2,'Мария','Петрова','mariapetrova','Pass12345'),(3,'Алексей','Сидоров','alexeysidorov','Pass12345'),(4,'Елена','Васильева','elenavasilyeva','Pass12345');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `teacher_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `patronymic` varchar(255) DEFAULT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'Сергей','Михайлов','Александрович','sergeymikhailov','Pass12345'),(2,'Ольга','Николаева','Игоревна','olganikolaeva','Pass12345'),(3,'Дмитрий','Козлов','Викторович','dmitrykozlov','Pass12345'),(4,'Ирина','Жукова','Петровна','irinazhukova','Pass12345');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usagereports`
--

DROP TABLE IF EXISTS `usagereports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usagereports` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  `period` varchar(255) NOT NULL,
  `auth_config_id` int NOT NULL,
  `log_id` int NOT NULL,
  PRIMARY KEY (`report_id`),
  KEY `auth_config_id` (`auth_config_id`),
  KEY `log_id` (`log_id`),
  KEY `student_id` (`student_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `usagereports_ibfk_1` FOREIGN KEY (`auth_config_id`) REFERENCES `authconfigs` (`config_id`),
  CONSTRAINT `usagereports_ibfk_2` FOREIGN KEY (`log_id`) REFERENCES `actionlogs` (`log_id`),
  CONSTRAINT `usagereports_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `usagereports_ibfk_4` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usagereports`
--

LOCK TABLES `usagereports` WRITE;
/*!40000 ALTER TABLE `usagereports` DISABLE KEYS */;
INSERT INTO `usagereports` VALUES (13,1,NULL,'2024-01',1,9),(14,2,NULL,'2024-02',1,10),(15,NULL,1,'2024-03',1,11),(16,NULL,2,'2024-04',1,12);
/*!40000 ALTER TABLE `usagereports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `virtualmachines`
--

DROP TABLE IF EXISTS `virtualmachines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `virtualmachines` (
  `vm_id` int NOT NULL AUTO_INCREMENT,
  `vm_name` varchar(255) NOT NULL,
  `image_id` int NOT NULL,
  `configuration_id` int NOT NULL,
  `status` varchar(255) NOT NULL,
  `creation_date` datetime NOT NULL,
  PRIMARY KEY (`vm_id`),
  KEY `image_id` (`image_id`),
  KEY `configuration_id` (`configuration_id`),
  CONSTRAINT `virtualmachines_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `images` (`image_id`),
  CONSTRAINT `virtualmachines_ibfk_2` FOREIGN KEY (`configuration_id`) REFERENCES `configurations` (`configuration_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `virtualmachines`
--

LOCK TABLES `virtualmachines` WRITE;
/*!40000 ALTER TABLE `virtualmachines` DISABLE KEYS */;
INSERT INTO `virtualmachines` VALUES (1,'VM1',1,1,'active','2024-03-27 19:09:06'),(2,'VM2',2,2,'inactive','2024-03-27 19:09:06'),(3,'VM3',3,3,'active','2024-03-27 19:09:06'),(4,'VM4',4,4,'inactive','2024-03-27 19:09:06');
/*!40000 ALTER TABLE `virtualmachines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vmaccess`
--

DROP TABLE IF EXISTS `vmaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vmaccess` (
  `access_id` int NOT NULL AUTO_INCREMENT,
  `vm_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  `access_type` varchar(255) NOT NULL,
  PRIMARY KEY (`access_id`),
  KEY `vm_id` (`vm_id`),
  KEY `student_id` (`student_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `vmaccess_ibfk_1` FOREIGN KEY (`vm_id`) REFERENCES `virtualmachines` (`vm_id`),
  CONSTRAINT `vmaccess_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `vmaccess_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vmaccess`
--

LOCK TABLES `vmaccess` WRITE;
/*!40000 ALTER TABLE `vmaccess` DISABLE KEYS */;
INSERT INTO `vmaccess` VALUES (1,1,1,NULL,'full'),(2,2,2,NULL,'read'),(3,3,NULL,1,'full'),(4,4,NULL,2,'read');
/*!40000 ALTER TABLE `vmaccess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vmstudents`
--

DROP TABLE IF EXISTS `vmstudents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vmstudents` (
  `vm_id` int NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`vm_id`,`student_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `vmstudents_ibfk_1` FOREIGN KEY (`vm_id`) REFERENCES `virtualmachines` (`vm_id`),
  CONSTRAINT `vmstudents_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vmstudents`
--

LOCK TABLES `vmstudents` WRITE;
/*!40000 ALTER TABLE `vmstudents` DISABLE KEYS */;
INSERT INTO `vmstudents` VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE `vmstudents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vmteachers`
--

DROP TABLE IF EXISTS `vmteachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vmteachers` (
  `vm_id` int NOT NULL,
  `teacher_id` int NOT NULL,
  PRIMARY KEY (`vm_id`,`teacher_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `vmteachers_ibfk_1` FOREIGN KEY (`vm_id`) REFERENCES `virtualmachines` (`vm_id`),
  CONSTRAINT `vmteachers_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vmteachers`
--

LOCK TABLES `vmteachers` WRITE;
/*!40000 ALTER TABLE `vmteachers` DISABLE KEYS */;
INSERT INTO `vmteachers` VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE `vmteachers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-29 18:22:57
