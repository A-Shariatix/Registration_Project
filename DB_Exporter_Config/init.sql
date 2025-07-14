create database if not exists users;

create user if not exists 'batman'@'%' identified by 'root';
grant all privileges on *.* to 'batman'@'%';

create user if not exists 'exporter'@'%' identified by 'root';
grant all privileges on *.* to 'exporter'@'%';

use users;

create table if not exists information(
    id int primary key auto_increment,
    username varchar(255),
    password varchar(255)
    );
