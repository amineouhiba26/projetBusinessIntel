-- Drop tables in correct order (reverse of foreign key dependencies)
DROP TABLE IF EXISTS views CASCADE;
DROP TABLE IF EXISTS date_dim CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS movie CASCADE;
