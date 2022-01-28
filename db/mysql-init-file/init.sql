create user 'root'@'%' identified with mysql_native_password by 'pass';
grant all privileges on *.* to 'root'@'%';
CREATE DATABASE mytest;
use mytest;

CREATE TABLE images(
                id INT AUTO_INCREMENT,
                userid VARCHAR(36) NOT NULL,
                cameraid VARCHAR(36) NOT NULL,
                setid INT NOT NULL,
                imgid VARCHAR(36) NOT NULL,
                saveddate datetime NOT NULL,
                PRIMARY KEY(id)
                );

CREATE TABLE bullets(
            bulletid INT AUTO_INCREMENT,
            imgid VARCHAR(36) NOT NULL,
            xposition INT NOT NULL,
            yposition INT NOT NULL,
            PRIMARY KEY(bulletid)
);

CREATE TABLE targets(
            targetid INT AUTO_INCREMENT,
            imgid VARCHAR(36) NOT NULL,
            xposition INT NOT NULL,
            yposition INT NOT NULL,
            rowlength INT NOT NULL,
            collength INT NOT NULL,
            PRIMARY KEY(targetid)
);


INSERT INTO images VALUES (NULL,"jisoo","jisooCamera1", 1,"6c553876-51d6-42f9-ae0b-ade36f6e3b5a",'1998-01-23 12:45:56');
INSERT INTO bullets VALUES (NULL,"6c553876-51d6-42f9-ae0b-ade36f6e3b5a",3,4);
INSERT INTO targets VALUES (NULL,"6c553876-51d6-42f9-ae0b-ade36f6e3b5a",3,4,5,6);