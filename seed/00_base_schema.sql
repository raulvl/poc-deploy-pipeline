-- seed/00_base_schema.sql
-- Punto de partida: las 3 BDs arrancan con el mismo schema.
-- A partir de aquí, las migraciones en el código generan divergencia entre ambientes.

CREATE SCHEMA IF NOT EXISTS poc;

SET search_path TO poc;

CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username    VARCHAR(100) NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE conversations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL,           -- FK se agrega en migration 002
    title       VARCHAR(255),
    started_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,       -- FK se agrega en migration 002
    content         TEXT NOT NULL,
    sent_at         TIMESTAMPTZ DEFAULT NOW()
);
