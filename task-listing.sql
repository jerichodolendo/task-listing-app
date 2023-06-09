DROP DATABASE IF EXISTS `task-listing`;
CREATE DATABASE IF NOT EXISTS `task-listing`;

CREATE USER 'administrator'@'localhost' IDENTIFIED BY 'admin';
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'user';

GRANT ALL ON `task-listing`.* TO 'administrator'@'localhost';
GRANT UPDATE, DELETE, INSERT, SELECT ON `task-listing`.* TO 'appuser'@'localhost';

USE `task-listing`;

CREATE TABLE IF NOT EXISTS `category`(
    `categoryid` INT(5) NOT NULL AUTO_INCREMENT, 
    `categoryname` VARCHAR(32) NOT NULL, 
    `categorydesc` VARCHAR(256),
    PRIMARY KEY(`categoryid`)
);

DELETE FROM `category`;

INSERT INTO `category` (`categoryid`, `categoryname`, `categorydesc`) VALUES
    (1, 'School and Studies', 'stuffs to do at school and study what i want to learn'),
    (2, 'Extracurricular Activities', 'activities outside school'),
    (3, 'Movies to Watch', NULL),
    (4, 'Games to Play', 'games i bought and need to play');


CREATE TABLE IF NOT EXISTS `task`( 
    `taskid` INT(5) NOT NULL AUTO_INCREMENT,
    `isdone` BOOLEAN NOT NULL,
    `taskname` VARCHAR(32) NOT NULL,
    `taskdesc` VARCHAR(256),
    `adddate` DATE NOT NULL,
    `duedate` DATE,
    `categoryid` INT(5),
    KEY `task_catid_fk` (`categoryid`),
    PRIMARY KEY(`taskid`),
    CONSTRAINT `task_catid_fk` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`)
);

DELETE FROM `task`;

INSERT INTO `task` (`taskid`, `taskname`, `taskdesc`, `adddate`, `duedate`, `isdone`, `categoryid`) VALUES
    (1, 'Badminton Practice', 'badminton practice for nationals', '21-04-02', '21-04-06', true, 2),
    (2, 'Filipino Exam', 'history and cultural significance of art in ph', '22-05-24', '22-06-02', false, 1),
    (3, 'Math Olympiad Registration', 'badminton practice for nationals', '22-05-25', '22-07-25', true, 2),
    (4, 'Doctor Strange WP', 'doctor strange watch party and marathon', '22-05-29', NULL, false, 3),
    (5, 'Pokemon Sword and Shield', NULL, '22-06-01', NULL, false, 4),
    (6, 'Buy Red Dead Redemption', NULL, '22-06-01', '22-08-01', false, 4);
