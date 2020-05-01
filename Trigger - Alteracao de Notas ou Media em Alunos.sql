USE BD_ESCOLA;

DELIMITER $$;
CREATE TRIGGER ALTERAR_NOTAS_MEDIA_BU BEFORE UPDATE
ON ALUNOS FOR EACH ROW 

BEGIN
   IF NEW.NOTA1 <> OLD.NOTA1 OR NEW.NOTA2 <> OLD.NOTA2 
     OR NEW.MEDIA <> OLD.MEDIA THEN
    SET NEW.MEDIA := (NEW.NOTA1 + NEW.NOTA2) / 2;
   END IF;
   
   SET NEW.DATA_ALTERACAO := NOW();
   
END $$;