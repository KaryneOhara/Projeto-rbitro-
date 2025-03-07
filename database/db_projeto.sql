create database db_projeto;
use db_projeto;

create table if not exists tb_arbitros (
arb_id int auto_increment primary key not null,
arb_nome varchar(45) not null,
arb_email varchar(155) not null,
arb_cpf varchar(45) not null,
arb_telefone varchar(45) not null,
arb_senha text not null
);

create table if not exists tb_contratantes (
con_id int auto_increment primary key not null,
con_nome varchar(45) not null,
con_email varchar(155) not null,
con_cpf varchar(45) not null,
con_telefone varchar(45) not null,
con_senha text not null
);
