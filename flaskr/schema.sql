drop table if exists news;
create table news (
    id integer primary key autoincrement,
    time timestamp not null default current_timestamp,
    bumpCount int default 0,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 10000
    )
);

drop table if exists tech;
create table tech (
    id integer primary key autoincrement,
    time timestamp not null default current_timestamp,
    bumpCount int default 0,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 10000
    )
);

drop table if exists offtopic;
create table offtopic (
    id integer primary key autoincrement,
    time timestamp not null default current_timestamp,
    bumpCount int default 0,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 10000
    )
);

drop table if exists images;
create table images (
    id integer primary key autoincrement,
    time timestamp not null default current_timestamp,
    bumpCount int default 0,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 100000
    )
);

drop table if exists tests;
create table tests (
    id integer primary key autoincrement,
    time timestamp not null default current_timestamp,
    bumpCount int default 0,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 100000
    )
);
