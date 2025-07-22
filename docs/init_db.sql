create database biobench;

create table public.tasks
(
    id   uuid  not null
        constraint tasks_pk
            primary key,
    body jsonb not null
);

