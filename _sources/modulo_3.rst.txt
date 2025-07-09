Módulo 3
==========

Triggers e Procedures do Projeto



Triggers e Procedures (T-SQL)
-----------------------------

Esta seção detalha os Triggers e Procedures desenvolvidos em T-SQL para garantir a integridade dos dados e automatizar lógicas complexas no banco de dados do projeto.

Trigger de Verificação de Especialização de Aldeão
----------------------------------------------------

Este trigger garante que um aldeão só possa ser inserido em uma tabela de especialização (como `bob_mago` ou `bob_construtor`) se o seu tipo na tabela `aldeao` for compatível.

**Função Principal: `fn_verifica_tipo_para_especializacao()`**

A função verifica o tipo do aldeão antes de uma inserção nas tabelas de especialização. Se o tipo não for compatível, a operação é cancelada e um erro é retornado.

.. code-block:: sql

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

**Triggers Associados**

Dois triggers são criados para executar a função `fn_verifica_tipo_para_especializacao()` antes de qualquer inserção nas tabelas `bob_mago` and `bob_construtor`.

.. code-block:: sql

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


Trigger de Limpeza de Especialização Antiga
-------------------------------------------

Este trigger é acionado quando o campo `tipo` de um aldeão é atualizado. Se o tipo for alterado, o trigger remove automaticamente o registro correspondente da tabela de especialização antiga, mantendo a consistência dos dados.

**Função Principal: `fn_limpa_especializacao_antiga()`**

A função verifica se o tipo do aldeão foi alterado. Em caso afirmativo, ela deleta a entrada da tabela de especialização anterior (`bob_mago` ou `bob_construtor`).

.. code-block:: sql

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

**Trigger Associado**

O trigger `tg_atualiza_tipo_aldeao` executa a função `fn_limpa_especializacao_antiga()` após a coluna `tipo` na tabela `aldeao` ser atualizada.

.. code-block:: sql

    DROP TRIGGER IF EXISTS tg_atualiza_tipo_aldeao ON aldeao;
    CREATE TRIGGER tg_atualiza_tipo_aldeao
    AFTER UPDATE OF tipo ON aldeao
    FOR EACH ROW
    EXECUTE FUNCTION fn_limpa_especializacao_antiga();

Vídeo de Demonstração
---------------------

Assista ao nosso vídeo de demonstração aqui: `Vídeo do módulo 3 no YouTube <https://youtu.be/wt3_RqkVgO4>`_
