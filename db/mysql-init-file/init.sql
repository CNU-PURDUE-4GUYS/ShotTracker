create user 'root'@'%' identified with mysql_native_password by 'pass';
grant all privileges on *.* to 'root'@'%';
CREATE DATABASE mytest;
use mytest;

CREATE TABLE target(
                 target_id INT AUTO_INCREMENT,
                 x INT,
                 y INT,
                 w INT,
                 h INT,
                 PRIMARY KEY(target_id));

INSERT INTO target(x, y, w, h) VALUES (32, 23, 10, 10);
INSERT INTO target(x, y, w, h) VALUES (493, 482, 10, 10);
INSERT INTO target(x, y, w, h) VALUES (239, 129, 10, 10);
