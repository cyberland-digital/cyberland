drop table if exists post;

create table post (
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    content varchar(10000) not null
);