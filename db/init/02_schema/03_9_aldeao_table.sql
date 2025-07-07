-- Tabela Aldeao (depende de Chunk)
-- Deve ser criada após as tabelas dependentes, mas antes dos relacionamentos

CREATE TABLE Aldeao (
    id_aldeao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    profissao VARCHAR(50) NOT NULL,
    nivel_profissao INT NOT NULL DEFAULT 1,
    vida_maxima INT NOT NULL DEFAULT 20,
    vida_atual INT NOT NULL DEFAULT 20,
    id_chunk INT REFERENCES Chunk(id_chunk) ON DELETE SET NULL ON UPDATE CASCADE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comentário: Esta tabela armazena informações sobre aldeões no jogo
-- Cada aldeão tem uma profissão e está localizado em um chunk específico
