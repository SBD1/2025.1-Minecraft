-- Criação de usuários e permissões
CREATE ROLE minecraft WITH LOGIN PASSWORD 'root_password';
GRANT ALL PRIVILEGES ON DATABASE "2025_1_Minecraft" TO minecraft;
