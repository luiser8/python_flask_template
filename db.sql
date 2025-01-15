create database glucose_tracker_db;

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

CREATE TABLE users_measurements (
    id serial PRIMARY KEY,
    user_id integer NOT NULL,
    date varchar NOT NULL,
    hour varchar NOT NULL,
    value integer NOT NULL,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE users_auth (
    id serial PRIMARY KEY,
    user_id integer NOT NULL UNIQUE,
    access_token varchar NOT NULL,
    refresh_token varchar NOT NULL,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE users_forgot_password (
    id serial PRIMARY KEY,
    user_id integer NOT NULL UNIQUE,
    code varchar NOT NULL,
    status boolean NULL DEFAULT true,
    createdat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);