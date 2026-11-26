-- creare user accesare db
CREATE USER "agronow-backend" WITH PASSWORD 'django123' CREATEDB;

-- privilegii
GRANT ALL PRIVILEGES ON DATABASE postgres TO "agronow-backend";

GRANT ALL ON SCHEMA public TO "agronow-backend";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "agronow-backend";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "agronow-backend";

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "agronow-backend";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "agronow-backend";
