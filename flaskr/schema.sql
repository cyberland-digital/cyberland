drop table if exists post;

create table post (
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    board varchar(1) not null,
    content varchar(10000) not null,
    replyto_id integer,
    foreign key (replyto_id) references post (id)
);