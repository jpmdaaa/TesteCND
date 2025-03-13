CREATE DATABASE filmes_db;

USE filmes_db;

CREATE TABLE analise_filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ator VARCHAR(255) NOT NULL,
    participacoes INT DEFAULT 0,
    genero VARCHAR(100) NOT NULL,
    frequencia_genero INT DEFAULT 0,
    bilheteria_total BIGINT DEFAULT 0
);

CREATE TABLE recomendacoes_filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filme_id INT,
    titulo VARCHAR(255),
    data_lancamento DATE,
    nota FLOAT
);