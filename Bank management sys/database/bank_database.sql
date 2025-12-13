CREATE DATABASE IF NOT EXISTS bank_management;
USE bank_management;

CREATE TABLE accounts (
    account_no INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    balance DECIMAL(10,2) DEFAULT 0.00
);
