create user 'root'@'%' identified with mysql_native_password by 'pass';
grant all privileges on *.* to 'root'@'%';
CREATE DATABASE mytest;
use mytest;


CREATE TABLE shootingsets(
                userid VARCHAR(36) NOT NULL,
                setid VARCHAR(36) NOT NULL,
                startedtime datetime NOT NULL,
                PRIMARY KEY(setid)
);

CREATE TABLE images(
                id INT AUTO_INCREMENT,
                userid VARCHAR(36) NOT NULL,
                cameraid VARCHAR(36) NOT NULL,
                setid VARCHAR(36) NOT NULL,
                imgid VARCHAR(36) NOT NULL,
                saveddate datetime NOT NULL,
                PRIMARY KEY(id)
                );

CREATE TABLE bullets(
            id INT AUTO_INCREMENT,
            imgid VARCHAR(36) NOT NULL,
            xposition INT NOT NULL,
            yposition INT NOT NULL,
            isnew BOOLEAN NOT NULL,
            PRIMARY KEY(id)
);

CREATE TABLE targets(
            id INT AUTO_INCREMENT,
            imgid VARCHAR(36) NOT NULL,
            point1 INT NOT NULL,
            point2 INT NOT NULL,
            point3 INT NOT NULL,
            point4 INT NOT NULL,
            PRIMARY KEY(id)
);
CREATE TABLE refers(
    setid VARCHAR(36),
    userid VARCHAR(36) NOT NULL,
    refid VARCHAR(36) NOT NULL,
    PRIMARY KEY(setid)
);


