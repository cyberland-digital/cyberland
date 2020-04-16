drop table if exists site_boards;
create table if not exists site_boards
(
    id   serial primary key,
    name varchar (15) unique ,
    slug varchar(2) unique ,
    character_limit integer not null default 1000,
    federated boolean
);

drop table if exists site_posts;
create table if not exists site_posts
(
    id        serial primary key,
    board_id  integer references site_boards(id),
    content   text,
    bumpCount integer default 0,
    replyTo   integer default 0,
    time      timestamp default now()
);


insert into site_boards (name, slug, character_limit, federated) values ('technology', 't', 10000, false);
insert into site_boards (name, slug, character_limit, federated) values ('offtopic', 'o', 10000, false);
insert into site_boards (name, slug, character_limit, federated) values ('client test', 'c', 10000, false);
insert into site_boards (name, slug, character_limit, federated) values ('images', 'i', 100000, false);
insert into site_boards (name, slug, character_limit, federated) values ('news', 'n', 500, false);
