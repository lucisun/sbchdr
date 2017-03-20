-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: sbchdr
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.12.04.1

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
-- Table structure for table `fan`
--

DROP TABLE IF EXISTS `fan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fan` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `location` varchar(24) NOT NULL,
  `description` varchar(24) NOT NULL,
  `speed` float NOT NULL,
  PRIMARY KEY (`tstamp`,`location`,`description`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fan`
--

LOCK TABLES `fan` WRITE;
/*!40000 ALTER TABLE `fan` DISABLE KEYS */;
/*!40000 ALTER TABLE `fan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface`
--

DROP TABLE IF EXISTS `interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interface` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `interfaceindx` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `intdescr` varchar(12) DEFAULT NULL,
  `type` varchar(18) DEFAULT NULL,
  `mtu` smallint(5) unsigned DEFAULT NULL,
  `speed` bigint(20) unsigned DEFAULT NULL,
  `phyaddr` varchar(21) NOT NULL,
  `adminstate` varchar(12) NOT NULL,
  `operstate` varchar(12) NOT NULL,
  `iflastchange` bigint(20) unsigned DEFAULT NULL,
  `inoctets` bigint(20) unsigned DEFAULT NULL,
  `inunicastpkts` bigint(20) unsigned DEFAULT NULL,
  `innonunicastpkts` bigint(20) unsigned DEFAULT NULL,
  `indiscard` bigint(20) unsigned DEFAULT NULL,
  `outerr` bigint(20) unsigned DEFAULT NULL,
  `outoctets` bigint(20) unsigned DEFAULT NULL,
  `outunicastpkts` bigint(20) unsigned DEFAULT NULL,
  `outnonunicastpkts` bigint(20) unsigned DEFAULT NULL,
  `outdiscards` bigint(20) unsigned DEFAULT NULL,
  `inerrors` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`tstamp`,`interfaceindx`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface`
--

LOCK TABLES `interface` WRITE;
/*!40000 ALTER TABLE `interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `networkutil`
--

DROP TABLE IF EXISTS `networkutil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `networkutil` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `nuindex` int(10) unsigned NOT NULL,
  `rxutil` decimal(9,6) NOT NULL,
  `txutil` decimal(9,6) NOT NULL,
  PRIMARY KEY (`tstamp`,`nuindex`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `networkutil`
--

LOCK TABLES `networkutil` WRITE;
/*!40000 ALTER TABLE `networkutil` DISABLE KEYS */;
/*!40000 ALTER TABLE `networkutil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessionagent`
--

DROP TABLE IF EXISTS `sessionagent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessionagent` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `Hostname` varchar(48) NOT NULL,
  `SystemType` varchar(8) NOT NULL,
  `Status` varchar(16) NOT NULL,
  `InboundActiveSessions` int(10) unsigned DEFAULT NULL,
  `InboundSessionRate` int(10) unsigned DEFAULT NULL,
  `OutboundActiveSessions` int(10) unsigned DEFAULT NULL,
  `OutboundSessionRate` int(10) unsigned DEFAULT NULL,
  `InboundSessionsAdmitted` int(10) unsigned DEFAULT NULL,
  `InboundSessionsNotAdmitted` int(10) unsigned DEFAULT NULL,
  `InboundConcurrentSessionsHigh` int(10) unsigned DEFAULT NULL,
  `InboundAverageSessionRate` float DEFAULT NULL,
  `OutboundSessionsAdmitted` int(10) unsigned DEFAULT NULL,
  `OutboundSessionsNotAdmitted` int(10) unsigned DEFAULT NULL,
  `OutboundConcurrentSessionsHigh` int(10) unsigned DEFAULT NULL,
  `OutboundAverageSessionsRate` float DEFAULT NULL,
  `MaxBurstRate` float DEFAULT NULL,
  `TotalSeizures` float DEFAULT NULL,
  `TotalAnsweredSessions` bigint(20) DEFAULT NULL,
  `AnswerSeizureRatio` float DEFAULT NULL,
  `AverageOneWaySignalingLatency` float DEFAULT NULL,
  `MaximumOneWaySignalingLatency` float DEFAULT NULL,
  PRIMARY KEY (`tstamp`,`Hostname`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessionagent`
--

LOCK TABLES `sessionagent` WRITE;
/*!40000 ALTER TABLE `sessionagent` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessionagent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessionrealm`
--

DROP TABLE IF EXISTS `sessionrealm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessionrealm` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `RealmName` varchar(28) NOT NULL DEFAULT '',
  `InboundActiveSessions` int(10) unsigned DEFAULT NULL,
  `InboundSessionRate` int(10) unsigned DEFAULT NULL,
  `OutboundActiveSessions` int(10) unsigned DEFAULT NULL,
  `OutboundSessionRate` float unsigned DEFAULT NULL,
  `InboundSessionsAdmitted` int(10) unsigned DEFAULT NULL,
  `InboundSessionsNotAdmitted` int(10) unsigned DEFAULT NULL,
  `InboundConcurrentSessionsHigh` int(10) unsigned DEFAULT NULL,
  `InboundAverageSessionRate` float unsigned DEFAULT NULL,
  `OutboundSessionsAdmitted` int(10) unsigned DEFAULT NULL,
  `OutboundSessionsNotAdmitted` int(10) unsigned DEFAULT NULL,
  `OutboundConcurrentSessionsHigh` int(10) unsigned DEFAULT NULL,
  `OutboundAverageSessionsRate` float DEFAULT NULL,
  `MaxBurstRate` float DEFAULT NULL,
  `TotalSeizures` float DEFAULT NULL,
  `TotalAnsweredSessions` int(10) unsigned DEFAULT NULL,
  `AnswerSeizureRatio` float DEFAULT NULL,
  `AverageOneWaySignalingLatency` float DEFAULT NULL,
  `MaximumOneWaySignalingLatency` float DEFAULT NULL,
  `AverageQoSRFactor` float DEFAULT NULL,
  `MaximumQoSRFactor` float DEFAULT NULL,
  `CurrentQoSMajorExceeded` float DEFAULT NULL,
  `TotalQoSMajorExceeded` float DEFAULT NULL,
  `CurrentQoSCriticalExceeded` float DEFAULT NULL,
  `TotalQoSCriticalExceeded` float DEFAULT NULL,
  `EarlySession` int(10) unsigned DEFAULT NULL,
  `SuccessfulSessions` int(10) unsigned DEFAULT NULL,
  `ActiveSubscriptions` int(10) unsigned DEFAULT NULL,
  `SubscriptionsPerMax` int(10) unsigned DEFAULT NULL,
  `SubscriptionsHigh` int(10) unsigned DEFAULT NULL,
  `TotalSubscriptions` int(10) unsigned DEFAULT NULL,
  `ActiveLocalContacts` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`tstamp`,`RealmName`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessionrealm`
--

LOCK TABLES `sessionrealm` WRITE;
/*!40000 ALTER TABLE `sessionrealm` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessionrealm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sipinvites`
--

DROP TABLE IF EXISTS `sipinvites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sipinvites` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `messageevent` varchar(28) NOT NULL DEFAULT '',
  `servertotals` int(10) unsigned DEFAULT NULL,
  `clienttotals` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`tstamp`,`messageevent`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sipinvites`
--

LOCK TABLES `sipinvites` WRITE;
/*!40000 ALTER TABLE `sipinvites` DISABLE KEYS */;
/*!40000 ALTER TABLE `sipinvites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sipsessions`
--

DROP TABLE IF EXISTS `sipsessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sipsessions` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `sessions` int(10) unsigned DEFAULT NULL,
  `sessionsInitial` int(10) unsigned DEFAULT NULL,
  `sessionsEarly` int(10) unsigned DEFAULT NULL,
  `sessionsEstablished` int(10) unsigned DEFAULT NULL,
  `sessionsTerminated` int(10) unsigned DEFAULT NULL,
  `dialogs` int(10) unsigned DEFAULT NULL,
  `dialogsEarly` int(10) unsigned DEFAULT NULL,
  `dialogsConfirmed` int(10) unsigned DEFAULT NULL,
  `dialogsTerminated` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`tstamp`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sipsessions`
--

LOCK TABLES `sipsessions` WRITE;
/*!40000 ALTER TABLE `sipsessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sipsessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `space`
--

DROP TABLE IF EXISTS `space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `space` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `volumename` varchar(16) NOT NULL,
  `spaceused` int(11) NOT NULL,
  `spaceavailable` int(10) unsigned NOT NULL,
  PRIMARY KEY (`tstamp`,`volumename`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `space`
--

LOCK TABLES `space` WRITE;
/*!40000 ALTER TABLE `space` DISABLE KEYS */;
/*!40000 ALTER TABLE `space` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system`
--

DROP TABLE IF EXISTS `system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `cpu` float NOT NULL,
  `memory` float NOT NULL,
  `healthscore` float NOT NULL,
  `redundancystate` varchar(8) DEFAULT NULL,
  `signalsess` float NOT NULL,
  `cps` float NOT NULL,
  `camutilnat` float DEFAULT NULL,
  `camutilarp` float DEFAULT NULL,
  `i2cbuststate` varchar(16) DEFAULT NULL,
  `liccapacity` float NOT NULL,
  `currentcachedsiplocalcontactreg` int(10) unsigned NOT NULL,
  `currmgcppublendptgwreg` int(10) unsigned NOT NULL,
  `currh323numofreg` int(10) unsigned NOT NULL,
  `applloadrate` float DEFAULT NULL,
  `currdenyentriesallocated` int(10) unsigned NOT NULL,
  PRIMARY KEY (`tstamp`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system`
--

LOCK TABLES `system` WRITE;
/*!40000 ALTER TABLE `system` DISABLE KEYS */;
/*!40000 ALTER TABLE `system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperature`
--

DROP TABLE IF EXISTS `temperature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temperature` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `vtype` varchar(24) NOT NULL,
  `description` varchar(24) NOT NULL,
  `temperature` float NOT NULL,
  PRIMARY KEY (`tstamp`,`vtype`,`description`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperature`
--

LOCK TABLES `temperature` WRITE;
/*!40000 ALTER TABLE `temperature` DISABLE KEYS */;
/*!40000 ALTER TABLE `temperature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voltage`
--

DROP TABLE IF EXISTS `voltage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voltage` (
  `tstamp` char(10) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `vtype` varchar(24) NOT NULL,
  `description` varchar(24) NOT NULL,
  `voltage` float NOT NULL,
  PRIMARY KEY (`tstamp`,`vtype`,`description`),
  KEY `tstamp` (`tstamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voltage`
--

LOCK TABLES `voltage` WRITE;
/*!40000 ALTER TABLE `voltage` DISABLE KEYS */;
/*!40000 ALTER TABLE `voltage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-20  8:53:22
