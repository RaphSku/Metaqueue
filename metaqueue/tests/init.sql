create table metadata(
    id bigserial primary key,
    name varchar(30) not null check (name <> ''),
    timestamp timestamptz not null default now(),
    location varchar(30) not null check (location <> ''),
    context varchar(30) not null check (context <> '')
);