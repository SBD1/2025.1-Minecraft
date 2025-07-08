
-- Trigger para verificar se o tipo do aldeão é compatível com a especialização
CREATE OR REPLACE FUNCTION fn_verifica_tipo_para_especializacao()
RETURNS TRIGGER AS $$
DECLARE
    tipo_pai VARCHAR(50);
BEGIN
    IF TG_TABLE_NAME = 'bob_mago' THEN
        SELECT tipo INTO tipo_pai FROM aldeao WHERE id_aldeao = NEW.id_aldeao_mago;
        IF tipo_pai <> 'Mago' THEN
            RAISE EXCEPTION 'ERRO: Não é possível criar um Bob_mago. O Aldeão (ID: %) não é do tipo "Mago", mas sim "%".', NEW.id_aldeao_mago, tipo_pai;
        END IF;

    ELSIF TG_TABLE_NAME = 'bob_construtor' THEN
        SELECT tipo INTO tipo_pai FROM aldeao WHERE id_aldeao = NEW.id_aldeao_construtor;
        IF tipo_pai <> 'Construtor' THEN
            RAISE EXCEPTION 'ERRO: Não é possível criar um Bob_construtor. O Aldeão (ID: %) não é do tipo "Construtor", mas sim "%".', NEW.id_aldeao_construtor, tipo_pai;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_valida_insert_mago ON bob_mago;
CREATE TRIGGER tg_valida_insert_mago
BEFORE INSERT ON bob_mago
FOR EACH ROW
EXECUTE FUNCTION fn_verifica_tipo_para_especializacao();

DROP TRIGGER IF EXISTS tg_valida_insert_construtor ON bob_construtor;
CREATE TRIGGER tg_valida_insert_construtor
BEFORE INSERT ON bob_construtor
FOR EACH ROW
EXECUTE FUNCTION fn_verifica_tipo_para_especializacao();


CREATE OR REPLACE FUNCTION fn_limpa_especializacao_antiga()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.tipo IS DISTINCT FROM OLD.tipo THEN
        IF OLD.tipo = 'Mago' THEN
            DELETE FROM bob_mago WHERE id_aldeao_mago = OLD.id_aldeao;
        ELSIF OLD.tipo = 'Construtor' THEN
            DELETE FROM bob_construtor WHERE id_aldeao_construtor = OLD.id_aldeao;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_atualiza_tipo_aldeao ON aldeao;
CREATE TRIGGER tg_atualiza_tipo_aldeao
AFTER UPDATE OF tipo ON aldeao
FOR EACH ROW
EXECUTE FUNCTION fn_limpa_especializacao_antiga();