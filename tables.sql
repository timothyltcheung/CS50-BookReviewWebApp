CREATE TABLE users (
id SERIAL PRIMARY KEY,
username VARCHAR UNIQUE NOT NULL,
password VARCHAR NOT NULL
);

CREATE TABLE books (
ISBN VARCHAR PRIMARY KEY NOT NULL,
title VARCHAR NOT NULL,
author VARCHAR NOT NULL,
year VARCHAR NOT NULL
);

CREATE TABLE reviews (
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES users,
ISBN VARCHAR REFERENCES books,
review_score INTEGER NOT NULL,
review VARCHAR,
CHECK (review_score >=1 AND review_score <=5)
);
