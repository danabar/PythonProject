create database shop;
use shop;
create table Product (
product_id varchar(20) primary key,
product_Name varchar(100) not null,
product_expire_date datetime null,
product_size int null
);
create table Location (
location_id varchar(20) primary key,
city varchar(100) not null,
street varchar(100) not null,
building_number int null
);
create table ProductMovement (
movement_id varchar(20) primary key,
movement_time timestamp null,
from_location varchar(20) null,
to_location varchar(20) null,
product_id varchar(20) not null,
FOREIGN KEY (from_location) REFERENCES Location(location_id),
FOREIGN KEY (to_location) REFERENCES Location(location_id),
FOREIGN KEY (product_id) REFERENCES Product(product_id)
);