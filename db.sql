CREATE DATABASE example_db;

CREATE TABLE rol (
    id serial PRIMARY KEY,
    name varchar NOT NULL,
    status boolean NULL DEFAULT true,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    firstname varchar NOT NULL,
    lastname varchar NOT NULL,
    email varchar NOT NULL UNIQUE,
    password varchar NOT NULL,
    status boolean NULL DEFAULT true,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users_rol (
    id serial PRIMARY KEY,
    user_id integer NOT NULL,
    rol_id integer NOT NULL,
    status boolean NULL DEFAULT true,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (rol_id) REFERENCES rol (id)
);

CREATE TABLE resources_rol (
    id serial PRIMARY KEY,
    rol_id integer NOT NULL,
    resources varchar NOT NULL,
    status boolean NULL DEFAULT true,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES rol (id)
);
