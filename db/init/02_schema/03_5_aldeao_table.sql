-- Tabela Aldeao (depende de Chunk)
-- Deve ser criada após as tabelas dependentes, mas antes dos relacionamentos
-- Vila
CREATE TABLE Vila (
    id_vila SERIAL PRIMARY KEY,
    nome_vila VARCHAR(100),
    descricao_vila TEXT,
    id_chunk INTEGER NOT NULL UNIQUE,
    CONSTRAINT fk_vila_chunk FOREIGN KEY (id_chunk) REFERENCES chunk(id_chunk) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE Casa_aldeao (
    id_casa SERIAL PRIMARY KEY,
    descricao_casa TEXT,
    vila INTEGER NOT NULL,
    CONSTRAINT fk_casa_vila FOREIGN KEY (vila) REFERENCES vila(id_vila) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE Aldeao (
    id_aldeao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    profissao VARCHAR(50) NOT NULL,
    nivel_profissao INT NOT NULL DEFAULT 1,
    vida_maxima INT NOT NULL DEFAULT 20,
    vida_atual INT NOT NULL DEFAULT 20,
    id_casa INT REFERENCES Casa_aldeao(id_casa) ON DELETE SET NULL ON UPDATE CASCADE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Bob_mago (
    id_aldeao_mago INTEGER PRIMARY KEY,
    habilidade_mago VARCHAR(100),
    CONSTRAINT fk_mago_aldeao FOREIGN KEY (id_aldeao_mago) REFERENCES aldeao(id_aldeao) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE Bob_construtor (
    id_aldeao_construtor INTEGER PRIMARY KEY,
    habilidades_construtor TEXT,
    CONSTRAINT fk_construtor_aldeao FOREIGN KEY (id_aldeao_construtor) REFERENCES aldeao(id_aldeao) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

-- Comentário: Esta tabela armazena informações sobre aldeões no jogo
-- Cada aldeão tem uma profissão e está localizado em um chunk específico
