create database biobench;

create table public.tasks
(
    id   uuid  not null
        constraint tasks_pk
            primary key,
    body jsonb not null
);

create table public.assessments
(
    id                uuid not null
        constraint assessments_pk
            primary key,
    model             text not null,
    benchmark_version text not null
);

alter table public.assessments
    add complete boolean default FALSE not null;


create table public.complete_tasks
(
    task_id       uuid  not null
        constraint complete_tasks_tasks_id_fk
            references public.tasks
            on update cascade on delete cascade,
    assessment_id uuid  not null
        constraint complete_tasks_assessments_id_fk
            references public.assessments,
    result        jsonb not null
);

