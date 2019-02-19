DROP DATABASE IF EXISTS bookmark;
CREATE DATABASE bookmark
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;
USE bookmark;

CREATE TABLE entry(
id INTEGER AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(250) NOT NULL,
url VARCHAR(500) NOT NULL,
created INT NOT NULL,
doc TEXT
) DEFAULT CHARACTER SET utf8;