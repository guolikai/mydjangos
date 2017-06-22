#!/bin/bash
#Created on 2017-6-10 @Author:Guolikai
#Description:Docker Management System
MysqlConn='mysql -uroot -p123456'
DATABASE=shipman

CreateDatabase="Create database if not exists ${DATABASE} character set utf8;"
$MysqlConn -e "$CreateDatabase"

#创建User用户表
CreateUser="Create table ${DATABASE}.user(
    id int(2) auto_increment PRIMARY KEY,
    name varchar(32) NOT NULL,
    password varchar(32) NOT NULL,
    user_group varchar(32) NOT NULL default 'Admin')"

$MysqlConn -e "$CreateUser"
Descuser="desc ${DATABASE}.user"
$MysqlConn -e "$Descuser"

#insert into shipman.user (name,password,user_group) values('admin',md5('123456'),'Admin');
InsertUser1="insert into ${DATABASE}.user (name,password,user_group) values('admin',md5('123456'),'Admin');"
$MysqlConn -e "$InsertUser1"
nsertUser2="insert into ${DATABASE}.user (name,password) values('user01',md5('123456'));"
MysqlConn -e "$InsertUser2"
getuser="select * from ${DATABASE}.user;"
$MysqlConn -e "$getuser"


#创建Node节点表
CreateNode="Create table ${DATABASE}.node(
    id int(2) auto_increment  PRIMARY KEY,
    name varchar(32) NOT NULL,
    node_ip varchar(32) NOT NULL,
    port varchar(32) NOT NULL,
    cpus varchar(32) NOT NULL,,
    mem varchar(32) NOT NULL,
    images varchar(32) NOT NULL,
    state varchar(32) NOT NULL,
    node_group varchar(32) NOT NULL default 'Online'
    containers varchar(32) NOT NULL,
    os_version varchar(32) NOT NULL,
    kernel_version varchar(32) NOT NULL,
    docker_version varchar(32) NOT NULL)"
$MysqlConn -e "$CreateNode"
#insert into shipman.node (name,node_ip,port,node_group) values('text101','172.16.1.101','2375','Online');
#insert into shipman.node (name,node_ip,port,node_group) values('localhost','127.0.0.1','2375','Online');

#创建Con_Usage容器表
CreateConUsage="Create table ${DATABASE}.con_usage(
    id int(2) auto_increment  PRIMARY KEY,
    con_id varchar(32) NOT NULL,
    con_ip varchar(32) NOT NULL,
    con_name varchar(32) NOT NULL,
    node_ip varchar(32) NOT NULL,
    user_name varchar(32) NOT NULL,
    con_app   varchar(32) NOT NULL,
    con_desc varchar(32) NOT NULL)"
$MysqlConn -e "$CreateConUsage"

#备份数据库
#mysqldump -uroot -p123456 ${DATABASE} > /root/${DATABASE}.sql




