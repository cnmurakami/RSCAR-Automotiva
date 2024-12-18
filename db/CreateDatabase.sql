CREATE DATABASE  IF NOT EXISTS `rscarautomotive` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `rscarautomotive`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: rscarautomotive
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `cpf` varchar(14) DEFAULT NULL,
  `cnpj` varchar(18) DEFAULT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `razao_social` varchar(100) DEFAULT NULL,
  `endereco` varchar(255) NOT NULL,
  `telefone` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=2001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordem`
--

DROP TABLE IF EXISTS `ordem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordem` (
  `id_ordem` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `id_veiculo` int DEFAULT NULL,
  `id_status` int DEFAULT '0',
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_ordem`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_veiculo` (`id_veiculo`),
  KEY `ordem_ibfk_3` (`id_status`),
  CONSTRAINT `ordem_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `ordem_ibfk_2` FOREIGN KEY (`id_veiculo`) REFERENCES `veiculo` (`id_veiculo`),
  CONSTRAINT `ordem_ibfk_3` FOREIGN KEY (`id_status`) REFERENCES `status_servico` (`id_status`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=2001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordem`
--

LOCK TABLES `ordem` WRITE;
/*!40000 ALTER TABLE `ordem` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peca`
--

DROP TABLE IF EXISTS `peca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peca` (
  `id_peca` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `qtd` int DEFAULT '0',
  `valor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_peca`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peca`
--

LOCK TABLES `peca` WRITE;
/*!40000 ALTER TABLE `peca` DISABLE KEYS */;
INSERT INTO `peca` VALUES (1,'Pastilha Diant Lado Direito',5,75.00),(2,'Pastilha Diant Lado Esquerdo',2,68.00),(3,'Pastilha Tras Lado Esquerdo',3,52.90),(4,'Pastilha Tras Lado Direito',7,46.70),(5,'Molas dianteiras',4,350.00),(6,'Molas traseiras',1,380.00),(7,'Lâmpada H7',15,30.00),(8,'Brucutu Esguicho do limpador',7,95.00);
/*!40000 ALTER TABLE `peca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peca_ordem`
--

DROP TABLE IF EXISTS `peca_ordem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peca_ordem` (
  `id_peca_ordem` int NOT NULL AUTO_INCREMENT,
  `id_ordem` int NOT NULL,
  `id_peca` int NOT NULL,
  `qtd` int DEFAULT '1',
  PRIMARY KEY (`id_peca_ordem`),
  KEY `fk_ordem` (`id_ordem`),
  KEY `fk_peca` (`id_peca`),
  CONSTRAINT `fk_ordem` FOREIGN KEY (`id_ordem`) REFERENCES `ordem` (`id_ordem`),
  CONSTRAINT `fk_peca` FOREIGN KEY (`id_peca`) REFERENCES `peca` (`id_peca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peca_ordem`
--

LOCK TABLES `peca_ordem` WRITE;
/*!40000 ALTER TABLE `peca_ordem` DISABLE KEYS */;
/*!40000 ALTER TABLE `peca_ordem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_servico`
--

DROP TABLE IF EXISTS `status_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_servico` (
  `id_status` int NOT NULL,
  `status` varchar(100) NOT NULL,
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_servico`
--

LOCK TABLES `status_servico` WRITE;
/*!40000 ALTER TABLE `status_servico` DISABLE KEYS */;
INSERT INTO `status_servico` VALUES (-1,'Cancelado'),(0,'Em Orçamento'),(1,'Em andamento'),(2,'Finalizado');
/*!40000 ALTER TABLE `status_servico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_servico`
--

DROP TABLE IF EXISTS `tipo_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_servico` (
  `id_servico` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_servico`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_servico`
--

LOCK TABLES `tipo_servico` WRITE;
/*!40000 ALTER TABLE `tipo_servico` DISABLE KEYS */;
INSERT INTO `tipo_servico` VALUES (1,'Troca de óleo',320.00),(3,'Troca de disco de Freio dianteiro',480.00),(4,'Troca Pastilhas de freio dianteiras',390.00),(5,'Troca de amortecedores porta malas',180.00),(6,'Mão de Obra',150.00),(7,'Troca de Módulo de Conforto',430.00),(8,'Troca de Velas de ignição',170.00),(9,'Troca de filtro de óleo',100.00),(10,'Troca de filtro de ar condicionado',80.00),(11,'Troca de filtro de combustível',80.00),(12,'Troca de filtro de boia de combustível',250.00),(13,'Troca de filtro de bomba de combustível',320.00);
/*!40000 ALTER TABLE `tipo_servico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_servico_ordem`
--

DROP TABLE IF EXISTS `tipo_servico_ordem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_servico_ordem` (
  `id_tp_servico_ordem` int NOT NULL AUTO_INCREMENT,
  `id_ordem` int DEFAULT NULL,
  `id_servico` int DEFAULT NULL,
  PRIMARY KEY (`id_tp_servico_ordem`),
  KEY `id_ordem` (`id_ordem`),
  KEY `id_servico` (`id_servico`),
  CONSTRAINT `tipo_servico_ordem_ibfk_1` FOREIGN KEY (`id_ordem`) REFERENCES `ordem` (`id_ordem`),
  CONSTRAINT `tipo_servico_ordem_ibfk_2` FOREIGN KEY (`id_servico`) REFERENCES `tipo_servico` (`id_servico`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_servico_ordem`
--

LOCK TABLES `tipo_servico_ordem` WRITE;
/*!40000 ALTER TABLE `tipo_servico_ordem` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo_servico_ordem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veiculo`
--

DROP TABLE IF EXISTS `veiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `veiculo` (
  `id_veiculo` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `placa` varchar(10) NOT NULL,
  `chassi` varchar(50) NOT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `ano_fabricacao` int NOT NULL,
  `ano_modelo` int DEFAULT NULL,
  `cor` varchar(50) NOT NULL,
  PRIMARY KEY (`id_veiculo`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `veiculo_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=2000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veiculo`
--

LOCK TABLES `veiculo` WRITE;
/*!40000 ALTER TABLE `veiculo` DISABLE KEYS */;
/*!40000 ALTER TABLE `veiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'rscarautomotive'
--

--
-- Dumping routines for database 'rscarautomotive'
--
/*!50003 DROP PROCEDURE IF EXISTS `associar_tp_serv_ordem` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `associar_tp_serv_ordem`(
		IN p_id_ordem INT,
        IN p_id_servico INT
)
BEGIN
		INSERT INTO tipo_servico_ordem (id_ordem, id_servico)
        VALUES (p_id_ordem, p_id_servico);
        
        SELECT "Tipo de serviço por ordem associada com sucesso" AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `inserir_cliente` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `inserir_cliente`(
    IN p_cpf VARCHAR(14),
    IN p_cnpj VARCHAR(18),
    IN p_nome VARCHAR(100),
    IN p_razao_social VARCHAR(100),
    IN p_endereco VARCHAR(255),
    IN p_telefone VARCHAR(20),
    IN p_email VARCHAR(100)
)
BEGIN
    INSERT INTO cliente (cpf, cnpj, nome, razao_social, endereco, telefone, email) 
    VALUES (p_cpf, p_cnpj, p_nome, p_razao_social, p_endereco, p_telefone, p_email);
    
    SELECT 'Cliente inserido com sucesso!' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `inserir_ordem_s` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `inserir_ordem_s`(
	IN p_id_cliente INT,
    IN p_id_veiculo INT
)
BEGIN
    INSERT INTO veiculo (id_cliente, id_veiculo) 
    VALUES ( p_id_cliente, p_id_veiculo);
    
    SELECT 'Ordem inserida com sucesso!' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `inserir_tp_servico` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `inserir_tp_servico`(
		IN p_nome VARCHAR(100),
        IN p_valor DECIMAL(10, 2)
)
BEGIN
		INSERT INTO tipo_servico (nome, valor)
        VALUES (p_nome, p_valor);
        
        SELECT "Tipo de serviço incluído com sucesso!" AS message;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `inserir_veiculo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `inserir_veiculo`(
	IN p_id_cliente INT,
    IN p_placa VARCHAR(10),
    IN p_chassi VARCHAR(50),
    IN p_marca VARCHAR(100),
    IN p_modelo VARCHAR(100),
    IN p_ano_fabricacao INT,
    IN p_ano_modelo INT,
    IN p_cor VARCHAR(50)
)
BEGIN
    INSERT INTO veiculo (id_cliente, placa, chassi, marca, modelo, ano_fabricacao, ano_modelo, cor) 
    VALUES ( p_id_cliente, p_placa, p_chassi, p_marca, p_modelo, p_ano_fabricacao, p_ano_modelo, p_cor);
    
    SELECT 'Veículo inserido com sucesso!' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `selecionar_cliente` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `selecionar_cliente`(
    IN p_nome VARCHAR(100),
	IN p_razao_social VARCHAR(100),
	IN p_email VARCHAR(100),
	IN p_telefone VARCHAR(20),
    IN p_cpf VARCHAR(14),
    IN p_cnpj VARCHAR(18)
)
BEGIN
	DECLARE cliente_encontrado INT;
    DECLARE p_parametro_lower VARCHAR(100);
    SET p_parametro_lower = LOWER(p_parametro);

    SELECT id_cliente INTO cliente_encontrado 
    FROM cliente 
    WHERE LOWER(nome) LIKE CONCAT('%', p_parametro_lower, '%') 
       OR LOWER(email) LIKE CONCAT('%', p_parametro_lower, '%') 
       OR telefone LIKE CONCAT('%', p_parametro, '%') 
       OR cpf LIKE CONCAT('%', p_parametro, '%') 
       OR cnpj LIKE CONCAT('%', p_parametro, '%')
    LIMIT 1;    
    
    IF cliente_encontrado IS NULL THEN
        SELECT id_cliente INTO cliente_encontrado FROM cliente WHERE nome = p_nome;
    END IF;
    IF cliente_encontrado IS NULL THEN
        SELECT id_cliente INTO cliente_encontrado FROM cliente WHERE razao_social = p_razao_social;
    END IF;
    IF cliente_encontrado IS NULL THEN
        SELECT id_cliente INTO cliente_encontrado FROM cliente WHERE email = p_email;
    END IF;
    IF cliente_encontrado IS NULL THEN
        SELECT id_cliente INTO cliente_encontrado FROM cliente WHERE telefone = p_telefone;
    END IF;
    IF cliente_encontrado IS NULL THEN
        SELECT id_cliente INTO cliente_encontrado FROM cliente WHERE cpf = p_cpf;
    END IF;
    IF cliente_encontrado IS NULL THEN
        SELECT id_cliente INTO cliente_encontrado FROM cliente WHERE cnpj = p_cnpj;
    END IF;
        
		IF cliente_encontrado IS NOT NULL THEN
		SELECT * FROM cliente WHERE id_cliente = cliente_encontrado;
        ELSE 
			SELECT 'Cliente não cadastrado na base' AS messagem;
        END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `selecionar_veiculo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `selecionar_veiculo`(
    IN p_placa VARCHAR(10),
    IN id_cliente int
)
BEGIN
	DECLARE veiculo_encontrado INT;
	DECLARE p_parametro_lower VARCHAR(100);
	SET p_parametro_lower = LOWER(p_parametro);
    SELECT COUNT(*) INTO veiculo_encontrado 
    FROM veiculo 
    WHERE LOWER(id_veiculo) LIKE CONCAT('%', p_parametro_lower, '%') 
       OR LOWER(placa) LIKE CONCAT('%', p_parametro_lower, '%') 
       OR LOWER(chassi) LIKE CONCAT('%', p_parametro_lower, '%') 
       OR id_cliente LIKE CONCAT('%', p_parametro, '%');
       
	IF veiculo_encontrado = 0 THEN
        SELECT COUNT(*) INTO veiculo_encontrado FROM veiculo WHERE placa = p_placa;
    END IF;
    IF veiculo_encontrado = 0 THEN
        SELECT COUNT(*) INTO veiculo_encontrado FROM veiculo WHERE id_cliente = p_id_cliente;
    END IF;
        
    IF veiculo_encontrado >= 1 THEN
        SELECT * FROM veiculo 
        WHERE (LOWER(id_veiculo) LIKE CONCAT('%', p_parametro_lower, '%') 
            OR LOWER(placa) LIKE CONCAT('%', p_parametro_lower, '%') 
            OR LOWER(chassi) LIKE CONCAT('%', p_parametro_lower, '%') 
            OR id_cliente LIKE CONCAT('%', p_parametro, '%'))
            OR (placa = p_placa AND id_cliente = p_id_cliente);
    ELSE 
        SELECT 'Veículo não encontrado para o cliente especificado ou placa inválida' AS mensagem;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-31 20:40:15
