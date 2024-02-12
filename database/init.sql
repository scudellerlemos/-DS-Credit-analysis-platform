CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE public.cotacoes
(
    id_log serial NOT NULL PRIMARY KEY,
    id_UUID uuid NOT NULL DEFAULT uuid_generate_v4(),
    data_cotacao date NOT NULL,
    metodo text NOT NULL,
    nome_cliente text NOT NULL,
    loan_limit integer NOT NULL,
    gender integer NOT NULL,
    loan_type integer NOT NULL,
    loan_purpose integer NOT NULL,
    credit_worthiness integer NOT NULL,
    open_credit integer NOT NULL,
    income numeric(15, 5) NOT NULL,
    valor_predito numeric(15, 5) NOT NULL,
    r2 numeric(15, 5) NOT NULL,
    rmse numeric(15, 5) NOT NULL,
    emprestimo_aprovado INTEGER
);

ALTER TABLE IF EXISTS public.cotacoes
    OWNER to postgres;
