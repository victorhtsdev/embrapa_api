

-- Serve para armazenar a informação da captura do arquivo
CREATE TABLE data_log (
    uuid VARCHAR(36) PRIMARY KEY,  -- Todos os registros relativos a captura terão este mesmo id
    object VARCHAR(255),
    record_date DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Armazena a data e a hora do arquivo capturado
    object_last_modified_date DATETIME  -- Armazena a data e a hora de moficação do arquivo, usado na lógica de decisão para fazer uma nova captura
);

-- Serve para armazenar a informação da captura de Producao.csv
CREATE TABLE producao (
    uuid VARCHAR(36) ,            -- UUID da captura
    id INT NOT NULL,
    control VARCHAR(50),
    produto VARCHAR(255),
    ano INT,
    quantidade DECIMAL(15, 2),
    tipo VARCHAR(50),                        -- Para identificar se é item ou é pai
    totalizador VARCHAR(255),                -- Para identificar a qual item pai se refere
    PRIMARY KEY (uuid, id,ano)
);

--Serve para armazenar a informação da captura de Comercio.csv
CREATE TABLE comercio (
    uuid VARCHAR(36) ,            -- UUID da captura
    id INT NOT NULL,
    control VARCHAR(50),
    produto VARCHAR(255),
    ano INT,
    quantidade DECIMAL(15, 2),
    tipo VARCHAR(50),                        -- Para identificar se é item ou é pai
    totalizador VARCHAR(255),                -- Para identificar a qual item pai se refere
    PRIMARY KEY (uuid, id,ano)
);


-- Serve para armazenar a informação da captura de Exp<objeto>.csv
CREATE TABLE exportacao (
    uuid VARCHAR(36) ,            -- UUID da captura
    id INT NOT NULL,
    object VARCHAR(255),
    pais VARCHAR(255),
    ano INT,
    quantidade DECIMAL(15, 2),
    valor DECIMAL(15, 2),
    PRIMARY KEY (uuid, id,ano)
);

-- Serve para armazenar a informação da captura de Imp<objeto>.csv
CREATE TABLE importacao (
    uuid VARCHAR(36) ,            -- UUID da captura
    id INT NOT NULL,
    object VARCHAR(255),
    pais VARCHAR(255),
    ano INT,
    quantidade DECIMAL(15, 2),
    valor DECIMAL(15, 2),
    PRIMARY KEY (uuid, id,ano)
);

CREATE TABLE processamento (
    uuid VARCHAR(36) ,            -- UUID da captura
    id INT NOT NULL,
    control VARCHAR(50),
    object VARCHAR(255),
    cultivar VARCHAR(255),
    ano INT,
    quantidade DECIMAL(15, 2),
    tipo VARCHAR(50),                        -- Para identificar se é item ou é pai
    totalizador VARCHAR(255),                -- Para identificar a qual item pai se refere
    PRIMARY KEY (uuid, id,ano)
);

CREATE TABLE usuarios (
    id CHAR(36) PRIMARY KEY,
    usuario VARCHAR(80) NOT NULL UNIQUE,
    senha VARCHAR(200) NOT NULL
);