CREATE DATABASE w3pw;
USE w3pw;
SOURCE w3pw.sql;

UPDATE main set pw=SHA1("secret");
