create user 'root'@'%' identified with mysql_native_password by 'pass';
grant all privileges on *.* to 'root'@'%';
CREATE DATABASE mytest;
use mytest;

CREATE TABLE images(
                id INT AUTO_INCREMENT NOT NULL,
                setid VARCHAR(36) NOT NULL,
                imgid VARCHAR(36) NOT NULL,
                saveddate datetime NOT NULL
                PRIMARY KEY(id)
                );

CREATE TABLE bullets(
            bulletid INT AUTO_INCREMENT NOT NULL,
            imgid VARCHAR(36) NOT NULL,
            PRIMARY KEY(bulletid)
)

CREATE TABLE targets(
            targetid INT AUTO_INCREMENT NOT NULL,
            imgid VARCHAR(36) NOT NULL,
            PRIMARY KEY(targetid)
)


INSERT INTO images VALUES (NULL,"3d7cd635-c41e-468a-b485-2147313a37d2", "3d7cd635-c41e-468a-b485-2147313a37d2", '1998-01-23 12:45:56', );
