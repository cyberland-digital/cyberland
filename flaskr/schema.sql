drop table if exists news;
create table news (
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    bumpCount int default null,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 10000
    )
);

drop table if exists tech;
create table tech (
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    bumpCount int default null,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 10000
    )
);

drop table if exists offtopic;
create table offtopic (
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    bumpCount int default null,
    content text not null,
    replyTo integer default null,

    check (
        length("content") <= 10000
    )
);
