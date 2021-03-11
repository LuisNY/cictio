begin;
drop DATABASE IF EXISTS cictio_db;
create DATABASE cictio_db;
USE cictio_db;

drop USER IF EXISTS cictio_user@localhost;
CREATE USER 'cictio_user'@'cictio_mysql' IDENTIFIED BY 'cictio';
GRANT ALL PRIVILEGES ON *.* TO 'cictio_user'@'cictio_mysql';
commit;