# syntax=docker/dockerfile:1

FROM postgres:13

RUN mkdir -p /docker-entrypoint-initdb.d

COPY init.sql ./docker-entrypoint-initdb.d